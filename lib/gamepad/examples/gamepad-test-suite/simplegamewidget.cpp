// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "simplegamewidget.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QPainter>
#include <QDateTime>
#include <cstdlib>

using namespace TreelandGamepad;
using namespace deckshell::deckgamepad;

SimpleGameWidget::SimpleGameWidget(TreelandGamepadClient *client, QWidget *parent)
    : QWidget(parent)
    , m_client(client)
{
    setMinimumSize(800, 600);
    setAutoFillBackground(true);
    QPalette pal = palette();
    pal.setColor(QPalette::Window, Qt::black);
    setPalette(pal);
    
    // UI布局
    auto *mainLayout = new QVBoxLayout(this);
    
    // 顶部信息栏
    auto *infoLayout = new QHBoxLayout;
    m_scoreLabel = new QLabel("得分: 0");
    m_scoreLabel->setStyleSheet("QLabel { color: white; font-size: 16px; }");
    infoLayout->addWidget(m_scoreLabel);
    
    m_livesLabel = new QLabel("生命: 3");
    m_livesLabel->setStyleSheet("QLabel { color: white; font-size: 16px; }");
    infoLayout->addWidget(m_livesLabel);
    
    infoLayout->addStretch();
    
    m_startButton = new QPushButton("开始游戏");
    connect(m_startButton, &QPushButton::clicked, this, &SimpleGameWidget::startGame);
    infoLayout->addWidget(m_startButton);
    
    mainLayout->addLayout(infoLayout);
    mainLayout->addStretch();
    
    resetGame();
}

SimpleGameWidget::~SimpleGameWidget()
{
    stopGame();
}

void SimpleGameWidget::setCurrentDevice(int deviceId)
{
    if (deviceId < 0) {
        m_currentDevice = nullptr;
        m_startButton->setEnabled(false);
        if (m_gameRunning) {
            stopGame();
        }
    } else {
        m_currentDevice = m_client->gamepad(deviceId);
        m_startButton->setEnabled(m_currentDevice != nullptr);
    }
}

void SimpleGameWidget::startGame()
{
    if (!m_currentDevice) return;
    
    resetGame();
    m_gameRunning = true;
    m_startButton->setText("停止游戏");
    disconnect(m_startButton, &QPushButton::clicked, this, &SimpleGameWidget::startGame);
    connect(m_startButton, &QPushButton::clicked, this, &SimpleGameWidget::stopGame);
    
    // 启动游戏循环
    m_timerId = startTimer(16); // ~60 FPS
}

void SimpleGameWidget::stopGame()
{
    m_gameRunning = false;
    if (m_timerId) {
        killTimer(m_timerId);
        m_timerId = 0;
    }
    
    m_startButton->setText("开始游戏");
    disconnect(m_startButton, &QPushButton::clicked, this, &SimpleGameWidget::stopGame);
    connect(m_startButton, &QPushButton::clicked, this, &SimpleGameWidget::startGame);
}

void SimpleGameWidget::resetGame()
{
    // 初始化玩家
    m_player.position = QPointF(width() / 2 - 25, height() - 100);
    m_player.size = QSizeF(50, 30);
    m_player.color = Qt::cyan;
    m_player.active = true;
    
    // 清空游戏对象
    m_bullets.clear();
    m_enemies.clear();
    
    // 重置状态
    m_score = 0;
    m_lives = 3;
    m_scoreLabel->setText("得分: 0");
    m_livesLabel->setText("生命: 3");
}

void SimpleGameWidget::timerEvent(QTimerEvent *event)
{
    Q_UNUSED(event)
    if (m_gameRunning) {
        updateGame();
    }
}

void SimpleGameWidget::paintEvent(QPaintEvent *event)
{
    Q_UNUSED(event)
    
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);
    
    if (!m_gameRunning) {
        painter.setPen(Qt::white);
        painter.setFont(QFont("Arial", 24));
        painter.drawText(rect(), Qt::AlignCenter, 
                        m_currentDevice ? "按开始按钮开始游戏" : "请先连接手柄");
        return;
    }
    
    // 绘制玩家
    if (m_player.active) {
        painter.fillRect(QRectF(m_player.position, m_player.size), m_player.color);
    }
    
    // 绘制子弹
    painter.setBrush(Qt::yellow);
    for (const auto &bullet : m_bullets) {
        if (bullet.active) {
            painter.drawEllipse(bullet.position, bullet.size.width() / 2, bullet.size.height() / 2);
        }
    }
    
    // 绘制敌人
    painter.setBrush(Qt::red);
    for (const auto &enemy : m_enemies) {
        if (enemy.active) {
            painter.drawRect(QRectF(enemy.position, enemy.size));
        }
    }
}

void SimpleGameWidget::updateGame()
{
    if (!m_currentDevice || !m_gameRunning) return;
    
    // 读取手柄输入
    double leftX = m_currentDevice->axisValue(GAMEPAD_AXIS_LEFT_X);
    double leftY = m_currentDevice->axisValue(GAMEPAD_AXIS_LEFT_Y);
    
    // 更新玩家位置
    const double speed = 5.0;
    m_player.position.rx() += leftX * speed;
    m_player.position.ry() += leftY * speed;
    
    // 限制在窗口内
    m_player.position.rx() = qBound(0.0, m_player.position.x(), 
                                    width() - m_player.size.width());
    m_player.position.ry() = qBound(0.0, m_player.position.y(), 
                                    height() - m_player.size.height());
    
    // 射击控制
    qint64 currentTime = QDateTime::currentMSecsSinceEpoch();
    if (m_currentDevice->axisValue(GAMEPAD_AXIS_TRIGGER_RIGHT) > 0.5 ||
        m_currentDevice->isButtonPressed(GAMEPAD_BUTTON_A)) {
        if (currentTime - m_lastFireTime > m_fireInterval) {
            fireBullet();
            m_lastFireTime = currentTime;
        }
    }
    
    // 更新子弹
    for (auto &bullet : m_bullets) {
        if (bullet.active) {
            bullet.position += bullet.velocity;
            if (bullet.position.y() < 0) {
                bullet.active = false;
            }
        }
    }
    
    // 移除非活动子弹
    m_bullets.erase(std::remove_if(m_bullets.begin(), m_bullets.end(),
                                   [](const GameObject &b) { return !b.active; }),
                   m_bullets.end());
    
    // 更新敌人
    for (auto &enemy : m_enemies) {
        if (enemy.active) {
            enemy.position += enemy.velocity;
            if (enemy.position.y() > height()) {
                enemy.active = false;
                // 漏掉敌人扣分
                m_score = qMax(0, m_score - 5);
                m_scoreLabel->setText(QString("得分: %1").arg(m_score));
            }
        }
    }
    
    // 移除非活动敌人
    m_enemies.erase(std::remove_if(m_enemies.begin(), m_enemies.end(),
                                   [](const GameObject &e) { return !e.active; }),
                   m_enemies.end());
    
    // 碰撞检测
    checkCollisions();
    
    // 随机生成敌人
    if (std::rand() % 100 < 2) {
        spawnEnemy();
    }
    
    update();
}

void SimpleGameWidget::checkCollisions()
{
    // 检查玩家与敌人碰撞
    for (auto &enemy : m_enemies) {
        if (!enemy.active) continue;
        
        QRectF playerRect(m_player.position, m_player.size);
        QRectF enemyRect(enemy.position, enemy.size);
        
        if (playerRect.intersects(enemyRect)) {
            enemy.active = false;
            m_lives--;
            m_livesLabel->setText(QString("生命: %1").arg(m_lives));
            
            // 振动反馈
            if (m_currentDevice) {
                m_currentDevice->setVibration(0.7, 1.0, 300);
            }
            
            if (m_lives <= 0) {
                stopGame();
                update();
            }
        }
    }
    
    // 检查子弹与敌人碰撞
    for (auto &bullet : m_bullets) {
        if (!bullet.active) continue;
        
        for (auto &enemy : m_enemies) {
            if (!enemy.active) continue;
            
            QRectF bulletRect(bullet.position - QPointF(bullet.size.width()/2, bullet.size.height()/2), 
                             bullet.size);
            QRectF enemyRect(enemy.position, enemy.size);
            
            if (bulletRect.intersects(enemyRect)) {
                bullet.active = false;
                enemy.active = false;
                m_score += 10;
                m_scoreLabel->setText(QString("得分: %1").arg(m_score));
                
                // 轻微振动反馈
                if (m_currentDevice) {
                    m_currentDevice->setVibration(0.3, 0.0, 50);
                }
                break;
            }
        }
    }
}

void SimpleGameWidget::spawnEnemy()
{
    GameObject enemy;
    enemy.position = QPointF(std::rand() % (width() - 40), -40);
    enemy.velocity = QPointF(0, 2 + std::rand() % 3);
    enemy.size = QSizeF(40, 40);
    enemy.color = Qt::red;
    enemy.active = true;
    
    m_enemies.append(enemy);
}

void SimpleGameWidget::fireBullet()
{
    GameObject bullet;
    bullet.position = m_player.position + QPointF(m_player.size.width() / 2, 0);
    bullet.velocity = QPointF(0, -10);
    bullet.size = QSizeF(5, 10);
    bullet.color = Qt::yellow;
    bullet.active = true;
    
    m_bullets.append(bullet);
}
