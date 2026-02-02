// SPDX-FileCopyrightText: 2024 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <deckshell/deckgamepad/backend/deckgamepadbackend.h>
#include <deckshell/deckgamepad/backend/sessiongate.h>
#include <deckshell/deckgamepad/mapping/deckgamepadsdlcontrollerdb.h>
#include <deckshell/deckgamepad/service/deckgamepadservice.h>

#include <QtCore/QCoreApplication>
#include <QtCore/QCommandLineParser>
#include <QtCore/QDateTime>
#include <QtCore/QDir>
#include <QtCore/QFileInfo>
#include <QtCore/QTimer>
#include <QtCore/QTextStream>
#include <QtCore/QFile>
#include <QtCore/QJsonDocument>
#include <QtCore/QJsonObject>
#include <QtCore/QJsonArray>

#include <sys/stat.h>
#include <unistd.h>

DECKGAMEPAD_USE_NAMESPACE

QTextStream cout(stdout);
QTextStream cerr(stderr);

static QString fileModeToOctalString(mode_t mode)
{
    const int bits = static_cast<int>(mode & 0777);
    return QStringLiteral("0%1").arg(bits, 3, 8, QLatin1Char('0'));
}

static QJsonObject statPath(const QString &path)
{
    QJsonObject obj;
    obj.insert(QStringLiteral("path"), path);

    struct stat st;
    if (::stat(path.toUtf8().constData(), &st) != 0) {
        obj.insert(QStringLiteral("exists"), false);
        return obj;
    }

    obj.insert(QStringLiteral("exists"), true);
    obj.insert(QStringLiteral("mode"), fileModeToOctalString(st.st_mode));
    obj.insert(QStringLiteral("uid"), static_cast<qint64>(st.st_uid));
    obj.insert(QStringLiteral("gid"), static_cast<qint64>(st.st_gid));
    obj.insert(QStringLiteral("size"), static_cast<qint64>(st.st_size));

    QFileInfo fi(path);
    obj.insert(QStringLiteral("readable"), fi.isReadable());
    obj.insert(QStringLiteral("writable"), fi.isWritable());
    obj.insert(QStringLiteral("executable"), fi.isExecutable());
    obj.insert(QStringLiteral("is_dir"), fi.isDir());
    obj.insert(QStringLiteral("is_file"), fi.isFile());

    return obj;
}

static QJsonObject errorToJson(const DeckGamepadError &error)
{
    QJsonObject obj;
    obj.insert(QStringLiteral("code"), static_cast<int>(error.code));
    obj.insert(QStringLiteral("message"), error.message);
    obj.insert(QStringLiteral("errno"), error.sysErrno);
    obj.insert(QStringLiteral("context"), error.context);
    obj.insert(QStringLiteral("hint"), error.hint);
    obj.insert(QStringLiteral("recoverable"), error.recoverable);
    return obj;
}

static QJsonObject diagnosticToJson(const DeckGamepadDiagnostic &diag)
{
    QJsonObject obj;
    obj.insert(QStringLiteral("key"), diag.key);
    obj.insert(QStringLiteral("details"), QJsonObject::fromVariantMap(diag.details));

    QJsonArray actions;
    for (const QString &a : diag.suggestedActions) {
        actions.append(a);
    }
    obj.insert(QStringLiteral("suggested_actions"), actions);

    return obj;
}

static int runDoctor()
{
    QJsonObject root;
    root.insert(QStringLiteral("schema_version"), QStringLiteral("1"));
    root.insert(QStringLiteral("generated_at_utc"), QDateTime::currentDateTimeUtc().toString(Qt::ISODateWithMs));

    QJsonObject build;
    build.insert(QStringLiteral("qt_version"), QString::fromLatin1(qVersion()));
#if defined(DECKGAMEPAD_ENABLE_LOGIND)
    build.insert(QStringLiteral("enable_logind"), static_cast<bool>(DECKGAMEPAD_ENABLE_LOGIND));
#else
    build.insert(QStringLiteral("enable_logind"), false);
#endif
    root.insert(QStringLiteral("build"), build);

    QJsonObject runtime;
    runtime.insert(QStringLiteral("uid"), static_cast<qint64>(::geteuid()));
    runtime.insert(QStringLiteral("gid"), static_cast<qint64>(::getegid()));
    runtime.insert(QStringLiteral("xdg_session_type"), qEnvironmentVariable("XDG_SESSION_TYPE"));
    runtime.insert(QStringLiteral("xdg_session_id"), qEnvironmentVariable("XDG_SESSION_ID"));
    runtime.insert(QStringLiteral("xdg_seat"), qEnvironmentVariable("XDG_SEAT"));
    runtime.insert(QStringLiteral("wayland_display"), qEnvironmentVariable("WAYLAND_DISPLAY"));
    runtime.insert(QStringLiteral("display"), qEnvironmentVariable("DISPLAY"));
    root.insert(QStringLiteral("runtime"), runtime);

    QJsonObject filesystem;
    filesystem.insert(QStringLiteral("dev_input"), statPath(QStringLiteral("/dev/input")));

    QJsonArray devInputEvents;
    QDir devInputDir(QStringLiteral("/dev/input"));
    const QStringList entries = devInputDir.entryList(QStringList{ QStringLiteral("event*") }, QDir::System | QDir::Files);
    for (const QString &name : entries.mid(0, 16)) {
        devInputEvents.append(statPath(devInputDir.absoluteFilePath(name)));
    }
    filesystem.insert(QStringLiteral("dev_input_events_sample"), devInputEvents);
    root.insert(QStringLiteral("filesystem"), filesystem);

    SessionGate gate;
    gate.setEnabled(true);
    QJsonObject session;
    session.insert(QStringLiteral("supported"), gate.supported());
    session.insert(QStringLiteral("active"), gate.isActive());
    root.insert(QStringLiteral("session_gate"), session);

    DeckGamepadService service;
    const bool ok = service.start();

    QJsonObject probe;
    probe.insert(QStringLiteral("start_ok"), ok);
    probe.insert(QStringLiteral("state"), static_cast<int>(service.state()));
    probe.insert(QStringLiteral("provider"), service.activeProviderName());
    probe.insert(QStringLiteral("known_gamepads"), static_cast<int>(service.knownGamepads().size()));
    probe.insert(QStringLiteral("connected_gamepads"), static_cast<int>(service.connectedGamepads().size()));
    probe.insert(QStringLiteral("error"), errorToJson(service.lastError()));
    probe.insert(QStringLiteral("diagnostic"), diagnosticToJson(service.diagnostic()));

    if (ok) {
        service.stop();
    }

    root.insert(QStringLiteral("service_probe"), probe);

    cout << QJsonDocument(root).toJson(QJsonDocument::Indented) << Qt::endl;

    // doctor 的目标是输出可复制的环境指纹；保持退出码稳定（用 start_ok 字段表达探测结果）。
    return 0;
}

class GamepadCli : public QObject
{
    Q_OBJECT

public:
    explicit GamepadCli(QObject *parent = nullptr)
        : QObject(parent)
        , m_backend(new DeckGamepadBackend(this))
        , m_testInputActive(false)
        , m_recording(false)
    {
        // Connect signals
        connect(m_backend, &DeckGamepadBackend::gamepadConnected,
                this, &GamepadCli::onGamepadConnected);
        connect(m_backend, &DeckGamepadBackend::gamepadDisconnected,
                this, &GamepadCli::onGamepadDisconnected);
        connect(m_backend, &DeckGamepadBackend::buttonEvent,
                this, &GamepadCli::onButtonEvent);
        connect(m_backend, &DeckGamepadBackend::axisEvent,
                this, &GamepadCli::onAxisEvent);
        connect(m_backend, &DeckGamepadBackend::hatEvent,
                this, &GamepadCli::onHatEvent);
    }

    bool start()
    {
        if (!m_backend->start()) {
            cerr << "Error: Failed to start gamepad backend" << Qt::endl;
            return false;
        }
        return true;
    }

    void listDevices()
    {
        QList<int> ids = m_backend->connectedGamepads();
        
        if (ids.isEmpty()) {
            cout << "No gamepads connected." << Qt::endl;
            QTimer::singleShot(0, qApp, &QCoreApplication::quit);
            return;
        }

        cout << "Connected Gamepads (" << ids.size() << "):" << Qt::endl;
        cout << "----------------------------------------" << Qt::endl;

        for (int id : ids) {
            DeckGamepadDevice *device = m_backend->device(id);
            if (device) {
                cout << "Device ID: " << id << Qt::endl;
                cout << "  Name: " << device->name() << Qt::endl;
                cout << "  Path: " << device->devicePath() << Qt::endl;
                cout << "  GUID: " << device->guid() << Qt::endl;
                
                if (device->hasSdlMapping()) {
                    cout << "  SDL Mapping: ✓ " << device->mappingName() << Qt::endl;
                } else {
                    cout << "  SDL Mapping: ✗ (using generic mapping)" << Qt::endl;
                }
                
                cout << Qt::endl;
            }
        }

        QTimer::singleShot(0, qApp, &QCoreApplication::quit);
    }

    void showDeviceInfo(int deviceId)
    {
        DeckGamepadDevice *device = m_backend->device(deviceId);
        if (!device) {
            cerr << "Error: Device " << deviceId << " not found" << Qt::endl;
            QTimer::singleShot(0, qApp, &QCoreApplication::quit);
            return;
        }

        cout << "Device Information:" << Qt::endl;
        cout << "==================" << Qt::endl;
        cout << "Device ID: " << deviceId << Qt::endl;
        cout << "Name: " << device->name() << Qt::endl;
        cout << "Path: " << device->devicePath() << Qt::endl;
        cout << "GUID: " << device->guid() << Qt::endl;
        cout << "Connected: " << (device->isConnected() ? "Yes" : "No") << Qt::endl;
        
        if (device->hasSdlMapping()) {
            cout << "SDL Mapping: ✓ Found" << Qt::endl;
            cout << "  Mapping Name: " << device->mappingName() << Qt::endl;
        } else {
            cout << "SDL Mapping: ✗ Not found" << Qt::endl;
            cout << "  Using: Generic Xbox layout" << Qt::endl;
        }

        cout << Qt::endl;
        cout << "SDL Database Status:" << Qt::endl;
        cout << "  Total Mappings: " << m_backend->sdlMappingCount() << Qt::endl;

        QTimer::singleShot(0, qApp, &QCoreApplication::quit);
    }

    void testVibration(int deviceId, float weak, float strong, int duration)
    {
        DeckGamepadDevice *device = m_backend->device(deviceId);
        if (!device) {
            cerr << "Error: Device " << deviceId << " not found" << Qt::endl;
            QTimer::singleShot(0, qApp, &QCoreApplication::quit);
            return;
        }

        cout << "Testing vibration on device " << deviceId << "..." << Qt::endl;
        cout << "  Weak: " << weak << Qt::endl;
        cout << "  Strong: " << strong << Qt::endl;
        cout << "  Duration: " << duration << " ms" << Qt::endl;

        if (m_backend->startVibration(deviceId, weak, strong, duration)) {
            cout << "Vibration started successfully!" << Qt::endl;
            
            // Auto-quit after vibration duration
            QTimer::singleShot(duration + 100, qApp, &QCoreApplication::quit);
        } else {
            cerr << "Error: Failed to start vibration (device may not support it)" << Qt::endl;
            QTimer::singleShot(0, qApp, &QCoreApplication::quit);
        }
    }

    void startInputTest(int deviceId = -1)
    {
        if (deviceId >= 0) {
            DeckGamepadDevice *device = m_backend->device(deviceId);
            if (!device) {
                cerr << "Error: Device " << deviceId << " not found" << Qt::endl;
                QTimer::singleShot(0, qApp, &QCoreApplication::quit);
                return;
            }
            m_testDeviceId = deviceId;
            cout << "Testing input from device " << deviceId << " (" << device->name() << ")" << Qt::endl;
        } else {
            m_testDeviceId = -1;
            cout << "Testing input from all devices" << Qt::endl;
        }

        cout << "Press Ctrl+C to stop" << Qt::endl;
        cout << "----------------------------------------" << Qt::endl;
        m_testInputActive = true;
    }

    bool startRecording(const QString &filename, int deviceId = -1)
    {
        if (filename.isEmpty()) {
            cerr << "Error: record filename is empty" << Qt::endl;
            return false;
        }

        m_recordFile.setFileName(filename);
        if (!m_recordFile.open(QIODevice::WriteOnly | QIODevice::Text | QIODevice::Truncate)) {
            cerr << "Error: Cannot write to file " << filename << Qt::endl;
            return false;
        }

        QJsonObject meta;
        meta["schema_version"] = "1.0";
        meta["type"] = "meta";
        meta["created_at"] = QDateTime::currentDateTimeUtc().toString(Qt::ISODateWithMs);
        writeRecordLine(meta);

        m_recording = true;
        cout << "Recording gamepad events to: " << filename << Qt::endl;
        startInputTest(deviceId);
        return true;
    }

    void showSdlDbInfo()
    {
        DeckGamepadSdlControllerDb *db = m_backend->sdlDb();
        if (!db) {
            cerr << "Error: SDL DB not available" << Qt::endl;
            QTimer::singleShot(0, qApp, &QCoreApplication::quit);
            return;
        }

        cout << "SDL GameController Database:" << Qt::endl;
        cout << "=============================" << Qt::endl;
        cout << "Total Mappings: " << db->mappingCount() << Qt::endl;
        cout << Qt::endl;

        // Show connected devices and their mapping status
        QList<int> ids = m_backend->connectedGamepads();
        if (!ids.isEmpty()) {
            cout << "Connected Devices:" << Qt::endl;
            for (int id : ids) {
                DeckGamepadDevice *device = m_backend->device(id);
                if (device) {
                    cout << "  " << device->name() << Qt::endl;
                    cout << "    GUID: " << device->guid() << Qt::endl;
                    cout << "    Mapped: " << (device->hasSdlMapping() ? "Yes" : "No") << Qt::endl;
                }
            }
        }

        QTimer::singleShot(0, qApp, &QCoreApplication::quit);
    }

    void queryGuid(const QString &guid)
    {
        DeckGamepadSdlControllerDb *db = m_backend->sdlDb();
        if (!db) {
            cerr << "Error: SDL DB not available" << Qt::endl;
            QTimer::singleShot(0, qApp, &QCoreApplication::quit);
            return;
        }

        cout << "Querying GUID: " << guid << Qt::endl;
        cout << "----------------------------------------" << Qt::endl;

        if (db->hasMapping(guid)) {
            QString name = db->getDeviceName(guid);
            cout << "✓ Mapping found!" << Qt::endl;
            cout << "  Device Name: " << name << Qt::endl;
        } else {
            cout << "✗ No mapping found for this GUID" << Qt::endl;
        }

        QTimer::singleShot(0, qApp, &QCoreApplication::quit);
    }

    void exportConfig(const QString &filename)
    {
        cout << "Exporting configuration to " << filename << "..." << Qt::endl;

        QJsonObject root;
        QJsonArray devices;

        QList<int> ids = m_backend->connectedGamepads();
        for (int id : ids) {
            DeckGamepadDevice *device = m_backend->device(id);
            if (device) {
                QJsonObject devObj;
                devObj["id"] = id;
                devObj["name"] = device->name();
                devObj["path"] = device->devicePath();
                devObj["guid"] = device->guid();
                devObj["has_sdl_mapping"] = device->hasSdlMapping();
                if (device->hasSdlMapping()) {
                    devObj["mapping_name"] = device->mappingName();
                }
                devices.append(devObj);
            }
        }

        root["devices"] = devices;
        root["sdl_db_mappings"] = m_backend->sdlMappingCount();
        root["export_timestamp"] = QDateTime::currentDateTime().toString(Qt::ISODate);

        QFile file(filename);
        if (!file.open(QIODevice::WriteOnly)) {
            cerr << "Error: Cannot write to file " << filename << Qt::endl;
            QTimer::singleShot(0, qApp, &QCoreApplication::quit);
            return;
        }

        QJsonDocument doc(root);
        file.write(doc.toJson(QJsonDocument::Indented));
        file.close();

        cout << "Configuration exported successfully!" << Qt::endl;
        cout << "  Devices: " << devices.size() << Qt::endl;

        QTimer::singleShot(0, qApp, &QCoreApplication::quit);
    }

private slots:
    void onGamepadConnected(int deviceId, const QString &name)
    {
        cout << "[CONNECTED] Device " << deviceId << ": " << name << Qt::endl;
    }

    void onGamepadDisconnected(int deviceId)
    {
        cout << "[DISCONNECTED] Device " << deviceId << Qt::endl;
    }

    void onButtonEvent(int deviceId, DeckGamepadButtonEvent event)
    {
        const bool matchDevice = (m_testDeviceId < 0 || deviceId == m_testDeviceId);

        if (m_recording && matchDevice) {
            QJsonObject obj;
            obj["schema_version"] = "1.0";
            obj["type"] = "button";
            obj["device_id"] = deviceId;
            obj["time_msec"] = int(event.time_msec);
            obj["button"] = int(event.button);
            obj["pressed"] = event.pressed;
            writeRecordLine(obj);
        }

        if (!m_testInputActive || !matchDevice) {
            return;
        }

        const char *buttonName = "UNKNOWN";
        switch (event.button) {
        case GAMEPAD_BUTTON_A: buttonName = "A"; break;
        case GAMEPAD_BUTTON_B: buttonName = "B"; break;
        case GAMEPAD_BUTTON_X: buttonName = "X"; break;
        case GAMEPAD_BUTTON_Y: buttonName = "Y"; break;
        case GAMEPAD_BUTTON_L1: buttonName = "L1"; break;
        case GAMEPAD_BUTTON_R1: buttonName = "R1"; break;
        case GAMEPAD_BUTTON_L2: buttonName = "L2"; break;
        case GAMEPAD_BUTTON_R2: buttonName = "R2"; break;
        case GAMEPAD_BUTTON_SELECT: buttonName = "SELECT"; break;
        case GAMEPAD_BUTTON_START: buttonName = "START"; break;
        case GAMEPAD_BUTTON_L3: buttonName = "L3"; break;
        case GAMEPAD_BUTTON_R3: buttonName = "R3"; break;
        case GAMEPAD_BUTTON_GUIDE: buttonName = "GUIDE"; break;
        case GAMEPAD_BUTTON_DPAD_UP: buttonName = "DPAD_UP"; break;
        case GAMEPAD_BUTTON_DPAD_DOWN: buttonName = "DPAD_DOWN"; break;
        case GAMEPAD_BUTTON_DPAD_LEFT: buttonName = "DPAD_LEFT"; break;
        case GAMEPAD_BUTTON_DPAD_RIGHT: buttonName = "DPAD_RIGHT"; break;
        default: break;
        }

        cout << "[BUTTON] Device " << deviceId << ": " << buttonName 
             << " " << (event.pressed ? "PRESSED" : "RELEASED") << Qt::endl;
    }

    void onAxisEvent(int deviceId, DeckGamepadAxisEvent event)
    {
        const bool matchDevice = (m_testDeviceId < 0 || deviceId == m_testDeviceId);

        if (m_recording && matchDevice) {
            QJsonObject obj;
            obj["schema_version"] = "1.0";
            obj["type"] = "axis";
            obj["device_id"] = deviceId;
            obj["time_msec"] = int(event.time_msec);
            obj["axis"] = int(event.axis);
            obj["value"] = event.value;
            writeRecordLine(obj);
        }

        if (!m_testInputActive || !matchDevice) {
            return;
        }

        // Only show significant axis changes (> 0.1)
        if (qAbs(event.value) < 0.1) return;

        const char *axisName = "UNKNOWN";
        switch (event.axis) {
        case GAMEPAD_AXIS_LEFT_X: axisName = "LEFT_X"; break;
        case GAMEPAD_AXIS_LEFT_Y: axisName = "LEFT_Y"; break;
        case GAMEPAD_AXIS_RIGHT_X: axisName = "RIGHT_X"; break;
        case GAMEPAD_AXIS_RIGHT_Y: axisName = "RIGHT_Y"; break;
        case GAMEPAD_AXIS_TRIGGER_LEFT: axisName = "TRIGGER_LEFT"; break;
        case GAMEPAD_AXIS_TRIGGER_RIGHT: axisName = "TRIGGER_RIGHT"; break;
        default: break;
        }

        cout << "[AXIS] Device " << deviceId << ": " << axisName 
             << " = " << QString::number(event.value, 'f', 3) << Qt::endl;
    }

    void onHatEvent(int deviceId, DeckGamepadHatEvent event)
    {
        const bool matchDevice = (m_testDeviceId < 0 || deviceId == m_testDeviceId);

        if (m_recording && matchDevice) {
            QJsonObject obj;
            obj["schema_version"] = "1.0";
            obj["type"] = "hat";
            obj["device_id"] = deviceId;
            obj["time_msec"] = int(event.time_msec);
            obj["hat"] = int(event.hat);
            obj["value"] = int(event.value);
            writeRecordLine(obj);
        }

        if (!m_testInputActive || !matchDevice) {
            return;
        }

        QStringList directions;
        if (event.value & GAMEPAD_HAT_UP) directions << "UP";
        if (event.value & GAMEPAD_HAT_RIGHT) directions << "RIGHT";
        if (event.value & GAMEPAD_HAT_DOWN) directions << "DOWN";
        if (event.value & GAMEPAD_HAT_LEFT) directions << "LEFT";

        QString dirStr = directions.isEmpty() ? "CENTER" : directions.join("+");
        cout << "[HAT] Device " << deviceId << ": " << dirStr << Qt::endl;
    }

private:
    void writeRecordLine(const QJsonObject &obj)
    {
        if (!m_recordFile.isOpen()) {
            return;
        }

        QJsonDocument doc(obj);
        m_recordFile.write(doc.toJson(QJsonDocument::Compact));
        m_recordFile.write("\n");
        m_recordFile.flush();
    }

    DeckGamepadBackend *m_backend;
    bool m_testInputActive;
    int m_testDeviceId;
    bool m_recording;
    QFile m_recordFile;
};

static bool replayTraceFile(const QString &filename)
{
    QFile file(filename);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        cerr << "Error: Cannot read file " << filename << Qt::endl;
        return false;
    }

    int count = 0;
    QTextStream in(&file);
    while (!in.atEnd()) {
        const QString line = in.readLine().trimmed();
        if (line.isEmpty()) {
            continue;
        }

        const QJsonDocument doc = QJsonDocument::fromJson(line.toUtf8());
        if (!doc.isObject()) {
            continue;
        }

        const QJsonObject obj = doc.object();
        const QString type = obj.value("type").toString();
        if (type == "meta") {
            continue;
        }

        const int deviceId = obj.value("device_id").toInt(-1);
        const int timeMsec = obj.value("time_msec").toInt(-1);

        if (type == "button") {
            const int button = obj.value("button").toInt(-1);
            const bool pressed = obj.value("pressed").toBool(false);
            cout << "[REPLAY][BUTTON] Device " << deviceId << " t=" << timeMsec << "ms"
                 << " button=" << button << " " << (pressed ? "PRESSED" : "RELEASED") << Qt::endl;
            count++;
        } else if (type == "axis") {
            const int axis = obj.value("axis").toInt(-1);
            const double value = obj.value("value").toDouble(0.0);
            cout << "[REPLAY][AXIS] Device " << deviceId << " t=" << timeMsec << "ms"
                 << " axis=" << axis << " value=" << QString::number(value, 'f', 3) << Qt::endl;
            count++;
        } else if (type == "hat") {
            const int hat = obj.value("hat").toInt(0);
            const int value = obj.value("value").toInt(0);

            QStringList directions;
            if (value & GAMEPAD_HAT_UP) directions << "UP";
            if (value & GAMEPAD_HAT_RIGHT) directions << "RIGHT";
            if (value & GAMEPAD_HAT_DOWN) directions << "DOWN";
            if (value & GAMEPAD_HAT_LEFT) directions << "LEFT";

            const QString dirStr = directions.isEmpty() ? "CENTER" : directions.join("+");
            cout << "[REPLAY][HAT] Device " << deviceId << " t=" << timeMsec << "ms"
                 << " hat=" << hat << " " << dirStr << Qt::endl;
            count++;
        }
    }

    cout << "Replay complete. Events: " << count << Qt::endl;
    return true;
}

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);
    app.setApplicationName("gamepad-config");
    app.setApplicationVersion("1.0.0");

    QCommandLineParser parser;
    parser.setApplicationDescription("DeckShell Gamepad Configuration Tool");
    parser.addHelpOption();
    parser.addVersionOption();

    // Command options
    QCommandLineOption listOption({"l", "list"}, "List all connected gamepads");
    parser.addOption(listOption);

    QCommandLineOption deviceOption({"d", "device"}, "Specify device ID", "id");
    parser.addOption(deviceOption);

    QCommandLineOption infoOption("info", "Show device information");
    parser.addOption(infoOption);

    QCommandLineOption vibrateOption("vibrate", 
        "Test vibration (format: weak,strong,duration_ms)", "params");
    parser.addOption(vibrateOption);

    QCommandLineOption testInputOption({"t", "test-input"}, 
        "Test input (shows button/axis events)");
    parser.addOption(testInputOption);

    QCommandLineOption recordOption("record", "Record events to JSONL file", "filename");
    parser.addOption(recordOption);

    QCommandLineOption replayOption("replay", "Replay events from JSONL file", "filename");
    parser.addOption(replayOption);

    QCommandLineOption doctorOption("doctor", "Print environment diagnostics (JSON) and exit");
    parser.addOption(doctorOption);

    QCommandLineOption sdlDbOption("sdl-db", "Show SDL GameController DB information");
    parser.addOption(sdlDbOption);

    QCommandLineOption queryGuidOption("query-guid", "Query SDL DB for a GUID", "guid");
    parser.addOption(queryGuidOption);

    QCommandLineOption exportOption({"e", "export"}, 
        "Export configuration to file", "filename");
    parser.addOption(exportOption);

    parser.process(app);

    if (parser.isSet(doctorOption)) {
        return runDoctor();
    }

    if (parser.isSet(replayOption)) {
        const QString filename = parser.value(replayOption);
        return replayTraceFile(filename) ? 0 : 1;
    }

    GamepadCli cli;
    if (!cli.start()) {
        return 1;
    }

    // Wait a bit for devices to be detected
    QTimer::singleShot(500, [&]() {
        if (parser.isSet(listOption)) {
            cli.listDevices();
        }
        else if (parser.isSet(infoOption)) {
            int deviceId = parser.value(deviceOption).toInt();
            cli.showDeviceInfo(deviceId);
        }
        else if (parser.isSet(vibrateOption)) {
            int deviceId = parser.value(deviceOption).toInt();
            QString params = parser.value(vibrateOption);
            QStringList parts = params.split(',');
            
            if (parts.size() != 3) {
                cerr << "Error: vibrate parameter must be: weak,strong,duration_ms" << Qt::endl;
                qApp->quit();
                return;
            }
            
            float weak = parts[0].toFloat();
            float strong = parts[1].toFloat();
            int duration = parts[2].toInt();
            
            cli.testVibration(deviceId, weak, strong, duration);
        }
        else if (parser.isSet(recordOption)) {
            const QString filename = parser.value(recordOption);
            const int deviceId = parser.isSet(deviceOption) ? parser.value(deviceOption).toInt() : -1;
            if (!cli.startRecording(filename, deviceId)) {
                QTimer::singleShot(0, qApp, &QCoreApplication::quit);
            }
        }
        else if (parser.isSet(testInputOption)) {
            int deviceId = parser.isSet(deviceOption) ? parser.value(deviceOption).toInt() : -1;
            cli.startInputTest(deviceId);
        }
        else if (parser.isSet(sdlDbOption)) {
            cli.showSdlDbInfo();
        }
        else if (parser.isSet(queryGuidOption)) {
            QString guid = parser.value(queryGuidOption);
            cli.queryGuid(guid);
        }
        else if (parser.isSet(exportOption)) {
            QString filename = parser.value(exportOption);
            cli.exportConfig(filename);
        }
        else {
            parser.showHelp(0);
        }
    });

    return app.exec();
}

#include "main.moc"
