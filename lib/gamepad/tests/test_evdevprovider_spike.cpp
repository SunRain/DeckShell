// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <deckshell/deckgamepad/providers/evdev/evdevprovider.h>
#include <deckshell/deckgamepad/mapping/deckgamepadcustommappingmanager.h>

#include <QtCore/QMetaObject>
#include <QtCore/QThread>
#include <QtTest/QTest>

#include <type_traits>
#include <utility>

namespace {
bool isSingleThreadForcedByEnv()
{
    const QByteArray raw = qgetenv("DECKGAMEPAD_EVDEV_SINGLE_THREAD");
    if (raw.isEmpty()) {
        return false;
    }

    const QByteArray normalized = raw.trimmed().toLower();
    if (normalized.isEmpty()) {
        return true;
    }
    if (normalized == QByteArrayLiteral("0")
        || normalized == QByteArrayLiteral("false")
        || normalized == QByteArrayLiteral("no")
        || normalized == QByteArrayLiteral("off")) {
        return false;
    }
    return true;
}

template <typename Func>
auto invokeBlocking(QObject *target, Func &&func)
{
    using Ret = std::invoke_result_t<Func>;

    if (!target) {
        if constexpr (!std::is_void_v<Ret>) {
            return Ret{};
        } else {
            return;
        }
    }

    if (QThread::currentThread() == target->thread()) {
        if constexpr (!std::is_void_v<Ret>) {
            return func();
        } else {
            func();
            return;
        }
    }

    if constexpr (std::is_void_v<Ret>) {
        QMetaObject::invokeMethod(target, std::forward<Func>(func), Qt::BlockingQueuedConnection);
        return;
    } else {
        Ret result{};
        QMetaObject::invokeMethod(target, [&] { result = func(); }, Qt::BlockingQueuedConnection);
        return result;
    }
}
}

class TestEvdevProviderSpike : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void ioThread_isRunning_andDifferent()
    {
        deckshell::deckgamepad::EvdevProvider provider;

        deckshell::deckgamepad::DeckGamepadRuntimeConfig cfg;
        cfg.providerSelection = deckshell::deckgamepad::DeckGamepadProviderSelection::Evdev;
        QVERIFY(provider.setRuntimeConfig(cfg));

        auto *ioThread = provider.findChild<QThread *>(QStringLiteral("DeckGamepadEvdevProviderIO"));
        if (isSingleThreadForcedByEnv()) {
            QVERIFY2(!ioThread, "EvdevProvider should not create an IO thread in single-thread mode");

            auto *mgr = provider.customMappingManager();
            QVERIFY2(mgr, "EvdevProvider should expose a custom mapping manager");
            QCOMPARE(mgr->thread(), QThread::currentThread());
            return;
        }
        QVERIFY2(ioThread, "EvdevProvider should create an IO thread");
        QVERIFY(ioThread->isRunning());
        QVERIFY(ioThread != QThread::currentThread());
    }

    void customMappingManager_livesInIoThread()
    {
        deckshell::deckgamepad::EvdevProvider provider;

        deckshell::deckgamepad::DeckGamepadRuntimeConfig cfg;
        cfg.providerSelection = deckshell::deckgamepad::DeckGamepadProviderSelection::Evdev;
        QVERIFY(provider.setRuntimeConfig(cfg));

        auto *ioThread = provider.findChild<QThread *>(QStringLiteral("DeckGamepadEvdevProviderIO"));
        auto *mgr = provider.customMappingManager();
        QVERIFY2(mgr, "EvdevProvider should expose a custom mapping manager");
        if (isSingleThreadForcedByEnv()) {
            QVERIFY2(!ioThread, "EvdevProvider should not create an IO thread in single-thread mode");
            QCOMPARE(mgr->thread(), QThread::currentThread());
            return;
        }
        QVERIFY2(ioThread, "EvdevProvider should create an IO thread");
        QVERIFY(ioThread->isRunning());
        QCOMPARE(mgr->thread(), ioThread);
    }

    void customMappingManager_backendCalls_areSafe()
    {
        deckshell::deckgamepad::EvdevProvider provider;

        deckshell::deckgamepad::DeckGamepadRuntimeConfig cfg;
        cfg.providerSelection = deckshell::deckgamepad::DeckGamepadProviderSelection::Evdev;
        QVERIFY(provider.setRuntimeConfig(cfg));

        auto *mgr = provider.customMappingManager();
        QVERIFY(mgr);

        // No devices in CI/容器环境时，也不应因跨线程访问而崩溃或死锁。
        QCOMPARE(invokeBlocking(mgr, [mgr] { return mgr->hasCustomMapping(0); }), false);
        QCOMPARE(invokeBlocking(mgr, [mgr] { return mgr->createCustomMapping(0); }), QString());
    }

    void startStop_isSafe()
    {
        deckshell::deckgamepad::EvdevProvider provider;

        // 不要求在 CI/容器中能真正启动 udev/evdev，只要求 start/stop 不崩溃且幂等。
        (void)provider.start();
        provider.stop();
        provider.stop();
    }
};

QTEST_MAIN(TestEvdevProviderSpike)
#include "test_evdevprovider_spike.moc"
