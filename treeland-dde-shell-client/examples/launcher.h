#ifndef LAUNCHER_H
#define LAUNCHER_H

#include <QWidget>

class QPushButton;
class QLabel;

class Launcher : public QWidget
{
    Q_OBJECT

public:
    explicit Launcher(QWidget *parent = nullptr);
    ~Launcher() override = default;

Q_SIGNALS:
    void widgetDemoRequested();
    void qmlDemoRequested();

private:
    void setupUI();

    QLabel *m_titleLabel;
    QLabel *m_descLabel;
    QPushButton *m_widgetBtn;
    QPushButton *m_qmlBtn;
};

#endif // LAUNCHER_H
