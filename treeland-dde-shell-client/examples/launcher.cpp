#include "launcher.h"

#include <QLabel>
#include <QPushButton>
#include <QVBoxLayout>

Launcher::Launcher(QWidget *parent)
    : QWidget(parent)
{
    setWindowTitle("DDE Shell Demo Launcher");
    setFixedSize(500, 400);
    setupUI();
}

void Launcher::setupUI()
{
    auto *layout = new QVBoxLayout(this);
    layout->setSpacing(20);
    layout->setContentsMargins(40, 40, 40, 40);

    // Title
    m_titleLabel = new QLabel("DDE Shell Demo", this);
    m_titleLabel->setAlignment(Qt::AlignCenter);
    m_titleLabel->setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;");
    layout->addWidget(m_titleLabel);

    // Description
    m_descLabel = new QLabel(
        "This demo showcases two ways to use DDE Shell:\n\n"
        "• Widget Demo - Traditional C++ Qt Widgets approach\n"
        "  Programmatic control with buttons and signals\n\n"
        "• QML Demo - Declarative QML approach\n"
        "  Using attached properties (layer-shell-qt style)",
        this);
    m_descLabel->setAlignment(Qt::AlignLeft);
    m_descLabel->setWordWrap(true);
    m_descLabel->setStyleSheet("font-size: 14px; color: #34495e; line-height: 1.6;");
    layout->addWidget(m_descLabel);

    layout->addStretch();

    // Widget Demo Button
    m_widgetBtn = new QPushButton("Launch Widget Demo", this);
    m_widgetBtn->setMinimumHeight(50);
    m_widgetBtn->setStyleSheet(
        "QPushButton {"
        "  font-size: 16px;"
        "  font-weight: bold;"
        "  background-color: #3498db;"
        "  color: white;"
        "  border: none;"
        "  border-radius: 5px;"
        "  padding: 10px;"
        "}"
        "QPushButton:hover {"
        "  background-color: #2980b9;"
        "}"
        "QPushButton:pressed {"
        "  background-color: #21618c;"
        "}");
    layout->addWidget(m_widgetBtn);

    // QML Demo Button
    m_qmlBtn = new QPushButton("Launch QML Demo", this);
    m_qmlBtn->setMinimumHeight(50);
    m_qmlBtn->setStyleSheet(
        "QPushButton {"
        "  font-size: 16px;"
        "  font-weight: bold;"
        "  background-color: #2ecc71;"
        "  color: white;"
        "  border: none;"
        "  border-radius: 5px;"
        "  padding: 10px;"
        "}"
        "QPushButton:hover {"
        "  background-color: #27ae60;"
        "}"
        "QPushButton:pressed {"
        "  background-color: #1e8449;"
        "}");
    layout->addWidget(m_qmlBtn);

    // Connect signals
    connect(m_widgetBtn, &QPushButton::clicked, this, &Launcher::widgetDemoRequested);
    connect(m_qmlBtn, &QPushButton::clicked, this, &Launcher::qmlDemoRequested);
}
