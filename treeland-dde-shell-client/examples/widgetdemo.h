#ifndef WIDGETDEMO_H
#define WIDGETDEMO_H

#include <QLabel>
#include <QMainWindow>
#include <QPointer>

class Window;
class QPushButton;

class WidgetDemo : public QMainWindow
{
    Q_OBJECT

public:
    explicit WidgetDemo(QWidget *parent = nullptr);
    ~WidgetDemo() override = default;

private:
    void setupUI();
    void setupDDEShell();

    QPointer<Window> m_ddeWindow;
    QLabel *m_statusLabel;

    // Control buttons
    QPushButton *m_skipMultitaskBtn;
    QPushButton *m_skipSwitcherBtn;
    QPushButton *m_skipDockBtn;
    QPushButton *m_acceptFocusBtn;
    QPushButton *m_setPositionBtn;

    // State tracking
    bool m_skipMultitask = true;
    bool m_skipSwitcher = false;
    bool m_skipDock = false;
    bool m_acceptFocus = true;
};

#endif // WIDGETDEMO_H
