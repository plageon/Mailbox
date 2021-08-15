import os
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QPushButton, QTextEdit, QFileDialog,QMessageBox


class SendWidget(QWidget):
    def __init__(self):
        super(SendWidget, self).__init__()
        self.setWindowTitle("Send E-mail")
        self.resize(800, 600)
        self.file_list = []

        self.sender_label = QLabel("Sender:", self)
        self.sender_label.resize(50, 20)
        self.sender_label.move(80, 50)

        self.license_label = QLabel("License:", self)
        self.license_label.resize(50, 20)
        self.license_label.move(80, 80)

        self.receiver_label = QLabel("Receiver:", self)
        self.receiver_label.resize(50, 20)
        self.receiver_label.move(80, 110)

        self.subject_label = QLabel("Subject:", self)
        self.subject_label.resize(50, 20)
        self.subject_label.move(80, 140)

        self.body_label = QLabel("Body:", self)
        self.body_label.resize(50, 20)
        self.body_label.move(80, 170)

        self.file_label = QLabel("Files:", self)
        self.file_label.resize(50, 20)
        self.file_label.move(80, 480)

        self.sender_edit = QLineEdit(self)
        self.sender_edit.resize(400, 20)
        self.sender_edit.move(150, 50)
        self.sender_edit.setText('zstanjj@163.com')

        self.license_edit = QLineEdit(self)
        self.license_edit.resize(400, 20)
        self.license_edit.move(150, 80)
        self.license_edit.setText('LVSXLRKYDWDHDFIJ')

        self.receiver_edit = QLineEdit(self)
        self.receiver_edit.resize(400, 20)
        self.receiver_edit.move(150, 110)
        self.receiver_edit.setPlaceholderText('Please seperate receivers with \';\'')
        self.receiver_edit.setText('2861803331@qq.com;zstanjj@outlook.com')

        self.subject_edit = QLineEdit(self)
        self.subject_edit.resize(400, 20)
        self.subject_edit.move(150, 140)
        self.subject_edit.setText("默认选中的按钮")

        self.body_edit = QTextEdit(self)
        self.body_edit.resize(400, 300)
        self.body_edit.move(150, 170)
        self.body_edit.setText("主要目的是运用计算机网络知识和基础的编程技能开发一款能满足用户各种邮箱业务需求的桌面应用。实验设计主要遵循保证满足用户各项使用需求，尽可能提高应用软件的适应性和鲁棒性，同时设计尽可能简单高效低冗余。")

        self.file_edit = QLineEdit(self)
        self.file_edit.resize(300, 20)
        self.file_edit.move(150, 480)

        self.file_button = QPushButton("Add File", self)
        self.file_button.resize(70, 20)
        self.file_button.move(470, 480)
        self.file_button.clicked.connect(self.select_file)

        self.send_button = QPushButton("Send!", self)
        self.send_button.resize(80, 50)
        self.send_button.move(200, 520)
        self.send_button.clicked.connect(self.send_mail)

    def select_file(self):
        file_name, file_type = QFileDialog.getOpenFileNames(self, "select file", "./",
                                                            "All Files (*);;Text Files (*.txt)")
        self.file_list += file_name
        file_text = ''
        for i in self.file_list:
            file_text += (i + ';')
        self.file_edit.setText(file_text)

    def send_mail(self):
        mail_host = "smtp." + self.sender_edit.text()[self.sender_edit.text().rfind('@') + 1:]
        mail_sender = self.sender_edit.text()
        mail_license = self.license_edit.text()
        mail_receivers = self.receiver_edit.text().split(';')

        mm = MIMEMultipart('related')
        subject_content = self.subject_edit.text()
        mm["From"] = "sender_name<" + self.sender_edit.text() + ">"
        receiver_text = ''
        for count, receiver in enumerate(self.receiver_edit.text().split(';')):
            receiver_text += ("receiver_" + str(count) + "_name<" + receiver + ">,")
        mm["To"] = receiver_text
        mm["Subject"] = Header(subject_content, 'utf-8')

        body_content = self.body_edit.toPlainText()
        message_text = MIMEText(body_content, "plain", "utf-8")
        mm.attach(message_text)

        for file in self.file_list:
            atta = MIMEText(open(file, 'rb').read(), 'base64', 'utf-8')
            file_name = os.path.basename(file)
            atta["Content-Disposition"] = 'attachment; filename=\"' + file_name + '\"'
            mm.attach(atta)

        try:
            stp = smtplib.SMTP()
            stp.connect(mail_host, 25)
            stp.set_debuglevel(1)
            stp.login(mail_sender, mail_license)
            stp.sendmail(mail_sender, mail_receivers, mm.as_string())
            # print('mail sent')
            send_info = QMessageBox.information(self,'Message','Mail sent!',QMessageBox.Yes)
            stp.quit()
        except:
            send_error = QMessageBox.warning(self,'Error','Invalid Arguments',QMessageBox.Yes)


