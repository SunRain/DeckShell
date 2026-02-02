// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <QWidget>
#include <QTimer>
#include <QLabel>
#include <QPushButton>
#include <QList>
#include "../../src/treelandgamepadclient.h"
#include "../../src/treelandgamepaddevice.h"

class SimpleGameWidget : public QWidget
{
    Q_OBJECT
    
public:
    explicit SimpleGameWidget(TreelandGamepad::TreelandGamepadClient *client,
                             QWidget *parent = nullptr);
    ~SimpleGameWidget();
    
public Q_SLOTS:
    void setCurrentDevice(int deviceId);
    
protected:
    void paintEvent(QPaintEvent *event) override;
    void timerEvent(QTimerEvent *event) override;
    
private Q_SLOTS:
    void startGame();
    void stopGame();
    
private:
    void updateGame();
    void checkCollisions();
    void spawnEnemy();
    void fireBullet();
    void resetGame();
    
    struct GameObject {
        QPointF position;
        QPointF velocity;
        QSizeF size;
        QColor color;
        bool active = true;
    };
    
private:
    TreelandGamepad::TreelandGamepadClient *m_client;
    TreelandGamepad::TreelandGamepadDevice *m_currentDevice = nullptr;
    
    int m_timerId = 0;
    GameObject m_player;
    QList<GameObject> m_bullets;
    QList<GameObject> m_enemies;
    
    int m_score = 0;
    int m_lives = 3;
    bool m_gameRunning = false;
    
    QLabel *m_scoreLabel;
    QLabel *m_livesLabel;
    QPushButton *m_startButton;
    
    // 控制状态
    qint64 m_lastFireTime = 0;
    const int m_fireInterval = 200; // 射击间隔ms
};
