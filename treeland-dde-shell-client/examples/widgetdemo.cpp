#include "widgetdemo.h"

#include <QDebug>
#include <QGridLayout>
#include <QGroupBox>
#include <QPushButton>
#include <QVBoxLayout>

#include <shellsurface.h>
#include <window.h>

WidgetDemo::WidgetDemo(QWidget *parent)
    : QMainWindow(parent)
{
    setWindowTitle("DDE Shell - Widget Demo");
    setFixedSize(500, 450);
    setupUI();
    setupDDEShell();
}

void WidgetDemo::setupUI()
{
    // Central widget
    QWidget *centralWidget = new QWidget(this);
    setCentralWidget(centralWidget);

    auto *mainLayout = new QVBoxLayout(centralWidget);
    mainLayout->setSpacing(15);
    mainLayout->setContentsMargins(20, 20, 20, 20);

    // Title
    auto *titleLabel = new QLabel("Widget Demo - C++ API", this);
    titleLabel->setAlignment(Qt::AlignCenter);
    titleLabel->setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;");
    mainLayout->addWidget(titleLabel);

    // Status label
    m_statusLabel = new QLabel("Initializing...", this);
    m_statusLabel->setAlignment(Qt::AlignCenter);
    m_statusLabel->setStyleSheet(
        "font-size: 14px; "
        "padding: 10px; "
        "background-color: #ecf0f1; "
        "border-radius: 5px;");
    mainLayout->addWidget(m_statusLabel);

    // Control group
    auto *controlGroup = new QGroupBox("DDE Shell Properties", this);
    auto *controlLayout = new QGridLayout(controlGroup);
    controlLayout->setSpacing(10);

    // Skip Multitask View button
    m_skipMultitaskBtn = new QPushButton("Skip Multitask View: ON", this);
    m_skipMultitaskBtn->setCheckable(true);
    m_skipMultitaskBtn->setChecked(true);
    controlLayout->addWidget(m_skipMultitaskBtn, 0, 0);

    // Skip Switcher button
    m_skipSwitcherBtn = new QPushButton("Skip Switcher: OFF", this);
    m_skipSwitcherBtn->setCheckable(true);
    m_skipSwitcherBtn->setChecked(false);
    controlLayout->addWidget(m_skipSwitcherBtn, 0, 1);

    // Skip Dock Preview button
    m_skipDockBtn = new QPushButton("Skip Dock Preview: OFF", this);
    m_skipDockBtn->setCheckable(true);
    m_skipDockBtn->setChecked(false);
    controlLayout->addWidget(m_skipDockBtn, 1, 0);

    // Accept Keyboard Focus button
    m_acceptFocusBtn = new QPushButton("Accept Focus: ON", this);
    m_acceptFocusBtn->setCheckable(true);
    m_acceptFocusBtn->setChecked(true);
    controlLayout->addWidget(m_acceptFocusBtn, 1, 1);

    // Set Position button
    m_setPositionBtn = new QPushButton("Set Position (400, 400)", this);
    controlLayout->addWidget(m_setPositionBtn, 2, 0, 1, 2);

    mainLayout->addWidget(controlGroup);

    // Info label
    auto *infoLabel = new QLabel(
        "Click buttons to toggle DDE Shell properties.\n"
        "Changes are applied immediately via C++ API.",
        this);
    infoLabel->setAlignment(Qt::AlignCenter);
    infoLabel->setWordWrap(true);
    infoLabel->setStyleSheet("font-size: 12px; color: #7f8c8d; font-style: italic;");
    mainLayout->addWidget(infoLabel);

    mainLayout->addStretch();

    // Connect button signals
    connect(m_skipMultitaskBtn, &QPushButton::toggled, this, [this](bool checked) {
        m_skipMultitask = checked;
        m_skipMultitaskBtn->setText(QString("Skip Multitask View: %1").arg(checked ? "ON" : "OFF"));
        if (m_ddeWindow) {
            m_ddeWindow->setSkipMultitaskview(checked);
            qDebug() << "Set skipMultitaskview:" << checked;
        }
    });

    connect(m_skipSwitcherBtn, &QPushButton::toggled, this, [this](bool checked) {
        m_skipSwitcher = checked;
        m_skipSwitcherBtn->setText(QString("Skip Switcher: %1").arg(checked ? "ON" : "OFF"));
        if (m_ddeWindow) {
            m_ddeWindow->setSkipSwitcher(checked);
            qDebug() << "Set skipSwitcher:" << checked;
        }
    });

    connect(m_skipDockBtn, &QPushButton::toggled, this, [this](bool checked) {
        m_skipDock = checked;
        m_skipDockBtn->setText(QString("Skip Dock Preview: %1").arg(checked ? "ON" : "OFF"));
        if (m_ddeWindow) {
            m_ddeWindow->setSkipDockPreview(checked);
            qDebug() << "Set skipDockPreview:" << checked;
        }
    });

    connect(m_acceptFocusBtn, &QPushButton::toggled, this, [this](bool checked) {
        m_acceptFocus = checked;
        m_acceptFocusBtn->setText(QString("Accept Focus: %1").arg(checked ? "ON" : "OFF"));
        if (m_ddeWindow) {
            m_ddeWindow->setAcceptKeyboardFocus(checked);
            qDebug() << "Set acceptKeyboardFocus:" << checked;
        }
    });

    connect(m_setPositionBtn, &QPushButton::clicked, this, [this]() {
        if (m_ddeWindow) {
            m_ddeWindow->setSurfacePosition(QPoint(400, 400));
            m_statusLabel->setText("Position set to (400, 400)");
            qDebug() << "Set surface position to (400, 400)";
        }
    });
}

void WidgetDemo::setupDDEShell()
{
    // Get DDE Shell Window wrapper
    m_ddeWindow = Window::get(this);

    if (!m_ddeWindow) {
        m_statusLabel->setText("Failed to create DDE Shell window");
        qWarning() << "Failed to get Window instance";
        return;
    }

    // Set initial properties
    m_ddeWindow->setSkipMultitaskview(m_skipMultitask);
    m_ddeWindow->setSkipSwitcher(m_skipSwitcher);
    m_ddeWindow->setSkipDockPreview(m_skipDock);
    m_ddeWindow->setAcceptKeyboardFocus(m_acceptFocus);
    m_ddeWindow->setRole(ShellSurface::Role::Overlay);

    // Monitor initialization signals
    connect(m_ddeWindow, &Window::initialized, this, [this]() {
        m_statusLabel->setText("✓ DDE Shell Initialized - Ready");
        m_statusLabel->setStyleSheet(
            "font-size: 14px; "
            "padding: 10px; "
            "background-color: #d5f4e6; "
            "color: #27ae60; "
            "border-radius: 5px;");
        qDebug() << "DDE Shell window initialized successfully";
    });

    connect(m_ddeWindow, &Window::initializationFailed, this, [this]() {
        m_statusLabel->setText("✗ DDE Shell Initialization Failed");
        m_statusLabel->setStyleSheet(
            "font-size: 14px; "
            "padding: 10px; "
            "background-color: #fadbd8; "
            "color: #c0392b; "
            "border-radius: 5px;");
        qWarning() << "DDE Shell window initialization failed";
    });

    // Check if already initialized
    if (m_ddeWindow->isInitialized()) {
        m_statusLabel->setText("✓ DDE Shell Already Initialized");
        m_statusLabel->setStyleSheet(
            "font-size: 14px; "
            "padding: 10px; "
            "background-color: #d5f4e6; "
            "color: #27ae60; "
            "border-radius: 5px;");
    }

    qDebug() << "DDE Shell properties configured";
}
