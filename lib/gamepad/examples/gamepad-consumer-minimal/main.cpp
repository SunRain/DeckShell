// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <deckshell/deckgamepad/service/deckgamepadservice.h>

#include <QtCore/QCommandLineParser>
#include <QtCore/QCoreApplication>
#include <QtCore/QDebug>
#include <QtCore/QTimer>

#include <cmath>

using deckshell::deckgamepad::DeckGamepadCapturePolicy;
using deckshell::deckgamepad::DeckGamepadProviderSelection;
using deckshell::deckgamepad::DeckGamepadRuntimeConfig;
using deckshell::deckgamepad::DeckGamepadService;

static DeckGamepadProviderSelection parseProviderSelection(const QString &value)
{
	const QString v = value.trimmed().toLower();
	if (v == QStringLiteral("auto")) {
		return DeckGamepadProviderSelection::Auto;
	}
	if (v == QStringLiteral("evdev")) {
		return DeckGamepadProviderSelection::Evdev;
	}
	if (v == QStringLiteral("evdev-udev") || v == QStringLiteral("evdev_udev") || v == QStringLiteral("udev")) {
		return DeckGamepadProviderSelection::EvdevUdev;
	}
	return DeckGamepadProviderSelection::Auto;
}

int main(int argc, char **argv)
{
	QCoreApplication app(argc, argv);
	app.setApplicationName(QStringLiteral("gamepad-consumer-minimal"));
	app.setApplicationVersion(QStringLiteral("1.0.0"));

	QCommandLineParser parser;
	parser.setApplicationDescription(QStringLiteral("Minimal DeckGamepad consumer demo (core/service only)"));
	parser.addHelpOption();
	parser.addVersionOption();

	const QCommandLineOption enableLegacyPathsOpt(QStringLiteral("enable-legacy-paths"),
	                                             QStringLiteral("Enable legacy DeckShell paths (~/.config/DeckShell/*)."));
	parser.addOption(enableLegacyPathsOpt);

	const QCommandLineOption captureAlwaysOpt(QStringLiteral("capture-always"),
	                                          QStringLiteral("Capture input even when not in active session (debug)."));
	parser.addOption(captureAlwaysOpt);

	const QCommandLineOption providerOpt({ QStringLiteral("p"), QStringLiteral("provider") },
	                                     QStringLiteral("Provider selection: auto|evdev|evdev-udev"),
	                                     QStringLiteral("provider"),
	                                     QStringLiteral("auto"));
	parser.addOption(providerOpt);

	const QCommandLineOption durationOpt({ QStringLiteral("d"), QStringLiteral("duration") },
	                                     QStringLiteral("Auto-exit after N seconds (0=run forever)."),
	                                     QStringLiteral("seconds"),
	                                     QStringLiteral("0"));
	parser.addOption(durationOpt);

	parser.process(app);

	bool durationOk = false;
	const int durationSeconds = parser.value(durationOpt).toInt(&durationOk);

	DeckGamepadService service;

	DeckGamepadRuntimeConfig cfg = service.runtimeConfig();
	cfg.enableLegacyDeckShellPaths = parser.isSet(enableLegacyPathsOpt);
	if (parser.isSet(captureAlwaysOpt)) {
		cfg.capturePolicy = DeckGamepadCapturePolicy::Always;
	}
	cfg.providerSelection = parseProviderSelection(parser.value(providerOpt));

	if (!service.setRuntimeConfig(cfg)) {
		qCritical() << "[deckgamepad] setRuntimeConfig failed:" << service.lastErrorMessage();
		return 1;
	}

	QObject::connect(&app, &QCoreApplication::aboutToQuit, &service, [&] {
		service.stop();
	});

	auto printErrorAndDiag = [&] {
		if (!service.lastErrorMessage().isEmpty()) {
			qWarning() << "[deckgamepad] lastErrorMessage=" << service.lastErrorMessage();
		}
		const auto diag = service.diagnostic();
		if (!diag.isOk()) {
			qWarning() << "[deckgamepad] diagnosticKey=" << diag.key
			           << "suggestedActions=" << diag.suggestedActions;
		}
	};

	QObject::connect(&service, &DeckGamepadService::lastErrorChanged, &service, [&] {
		printErrorAndDiag();
	});

	QObject::connect(&service, &DeckGamepadService::diagnosticChanged, &service, [&](auto) {
		printErrorAndDiag();
	});

	QObject::connect(&service, &DeckGamepadService::gamepadConnected, &service, [&](int deviceId, const QString &name) {
		qInfo() << "[deckgamepad] connected:" << deviceId << name;
	});

	QObject::connect(&service, &DeckGamepadService::gamepadDisconnected, &service, [&](int deviceId) {
		qInfo() << "[deckgamepad] disconnected:" << deviceId;
	});

	QObject::connect(&service, &DeckGamepadService::buttonEvent, &service, [&](int deviceId, auto ev) {
		qInfo() << "[deckgamepad] button device=" << deviceId << "button=" << ev.button
		        << (ev.pressed ? "pressed" : "released");
	});

	QObject::connect(&service, &DeckGamepadService::axisEvent, &service, [&](int deviceId, auto ev) {
		if (std::abs(ev.value) < 0.10) {
			return;
		}
		qInfo() << "[deckgamepad] axis device=" << deviceId << "axis=" << ev.axis << "value=" << ev.value;
	});

	QObject::connect(&service, &DeckGamepadService::hatEvent, &service, [&](int deviceId, auto ev) {
		if (ev.value == 0) {
			return;
		}
		qInfo() << "[deckgamepad] hat device=" << deviceId << "hat=" << ev.hat << "value=" << ev.value;
	});

	if (!service.start()) {
		qCritical() << "[deckgamepad] start failed:" << service.lastErrorMessage();
		printErrorAndDiag();
		return 1;
	}

	qInfo() << "[deckgamepad] started, provider=" << service.activeProviderName()
	        << "connected=" << service.connectedGamepads().size()
	        << "known=" << service.knownGamepads().size();
	printErrorAndDiag();

	if (durationOk && durationSeconds > 0) {
		QTimer::singleShot(durationSeconds * 1000, &app, &QCoreApplication::quit);
	}

	return app.exec();
}

