import email
import poplib
from email.header import decode_header
from email.parser import Parser
from email.utils import parseaddr

from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QPushButton, QFileDialog, QTextEdit, QMessageBox


class ReceiveWidget(QWidget):
    def __init__(self):
        super(ReceiveWidget, self).__init__()
        self.resize(800, 600)
        self.setWindowTitle("Receive E-mail")

        self.sender_label = QLabel("Sender:", self)
        self.sender_label.resize(50, 20)
        self.sender_label.move(80, 50)

        self.license_label = QLabel("License:", self)
        self.license_label.resize(50, 20)
        self.license_label.move(80, 80)

        self.file_label = QLabel("Directory:", self)
        self.file_label.resize(50, 20)
        self.file_label.move(80, 110)

        self.id_label = QLabel("Mail id:", self)
        self.id_label.resize(50, 20)
        self.id_label.move(80, 140)

        self.sender_edit = QLineEdit(self)
        self.sender_edit.resize(400, 20)
        self.sender_edit.move(150, 50)
        self.sender_edit.setText('zstanjj@163.com')

        self.license_edit = QLineEdit(self)
        self.license_edit.resize(400, 20)
        self.license_edit.move(150, 80)
        self.license_edit.setText('LVSXLRKYDWDHDFIJ')

        self.file_edit = QLineEdit(self)
        self.file_edit.resize(300, 20)
        self.file_edit.move(150, 110)
        self.file_edit.setPlaceholderText('select a directory to save attachments')

        self.body_edit = QTextEdit(self)
        self.body_edit.resize(400, 400)
        self.body_edit.move(150, 170)
        self.body_edit.setReadOnly(True)

        self.id_edit = QLineEdit(self)
        self.id_edit.resize(100, 20)
        self.id_edit.move(150, 140)
        self.id_edit.setPlaceholderText("ith mail")

        self.file_button = QPushButton("Target Dir", self)
        self.file_button.resize(70, 20)
        self.file_button.move(470, 110)
        self.file_button.clicked.connect(self.select_dir)

        self.check_button = QPushButton("Check", self)
        self.check_button.resize(50, 20)
        self.check_button.move(260, 140)
        self.check_button.clicked.connect(self.receive_mail)

        self.del_button = QPushButton("Delate", self)
        self.del_button.resize(50, 20)
        self.del_button.move(320, 140)
        self.del_button.clicked.connect(self.del_mail)

    def select_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "select file", "./")
        self.file_edit.setText(dir_path)

    def guess_charset(self, msg):
        charset = msg.get_charset()  # ??????msg????????????
        if charset is None:
            content_type = msg.get('Content-Type', '').lower()  # ???????????????????????????
            pos = content_type.find('charset=')  # ????????????????????????charset=?????????????????????
            if pos >= 0:
                charset = content_type[pos + 8:].strip()  # ????????????????????????????????????????????????
        return charset

    def decode_str(self, str):
        value, charset = decode_header(str)[0]  # Returns a list of (string, charset) pairs
        if charset:
            value = value.decode(charset)
        return value

    def get_att(self, msg, fpath):
        attachment_files = []

        for part in msg.walk():
            file_name = part.get_filename()  # ????????????????????????
            contType = part.get_content_type()

            if file_name:
                h = email.header.Header(file_name)
                dh = email.header.decode_header(h)  # ??????????????????????????????
                # Returns a list of (string, charset) pairs containing each of the decoded parts of the header
                filename = dh[0][0]
                if dh[0][1]:
                    filename = self.decode_str(str(filename, dh[0][1]))  # ????????????????????????
                    #print(filename)
                    # filename = filename.encode("utf-8")
                data = part.get_payload(decode=True)  # ????????????
                attachment_files.append(filename)
                with open(fpath + '/' + filename, 'wb') as att_file:  # ???????????????????????????????????????????????????????????????wb????????????
                    att_file.write(data)  # ????????????
        return attachment_files

    def print_info(self, msg, indent=0):
        mail = ''
        if indent == 0:
            for header in ['From', 'To', 'Subject']:
                value = msg.get(header, '')
                if value:
                    if header == 'Subject':
                        value = self.decode_str(value)
                    else:
                        hdr, addr = parseaddr(value)  # ????????????????????????realname???email address???????????????
                        name = self.decode_str(hdr)
                        value = u'%s <%s>' % (name, addr)  # u?????????????????????Unicode???????????????????????????????????????????????????????????????????????????
                mail += ('%s%s: %s\n' % ('  ' * indent, header, value))
        if (msg.is_multipart()):
            parts = msg.get_payload()
            for n, part in enumerate(parts):
                mail += ('%spart %s\n' % ('  ' * indent, n))
                mail += ('%s--------------------\n' % ('  ' * indent))
                self.print_info(part, indent + 1)
        else:
            content_type = msg.get_content_type()
            content = ''
            if content_type == 'text/plain' or content_type == 'text/html':
                content = msg.get_payload(decode=True)
                charset = self.guess_charset(msg)
                if charset:
                    content = content.decode(charset)
                mail += ('%sText: %s' % ('  ' * indent, content + '...'))
            else:
                mail += ('%sAttachment: %s' % ('  ' * indent, content_type))
        return mail

    def receive_mail(self):
        email = self.sender_edit.text()
        password = self.license_edit.text()  # ?????????????????????
        pop3_server = 'pop.' + self.sender_edit.text()[self.sender_edit.text().rfind('@') + 1:]
        server = poplib.POP3_SSL(pop3_server)
        server.set_debuglevel(1)
        # print(server.getwelcome().decode('utf-8'))
        server.user(email)
        server.pass_(password)
        # print('Messages: %s. Size: %s' % server.stat())
        resp, mails, octets = server.list()
        total = len(mails)
        id = int(self.id_edit.text())
        if id < total:
            index = total - id
            resp, lines, octets = server.retr(
                index)  # retr????????????????????????????????????????????????response???????????????????????????????????????????????????????????????????????????????????????????????????octets
            msg_content = b'\r\n'.join(lines).decode('utf-8')  # ??????line1\r\nline2\r\n ??????lines????????????????????????
            # ????????????:
            msg = Parser().parsestr(msg_content)
            # ??????????????????
            # date1 = time.strptime(msg.get("Date")[0:24], '%a, %d %b %Y %H:%M:%S')  # ?????????????????????
            # date2 = time.strftime("%Y%m%d", date1)  # ????????????????????????
            # print(msg.get("from"))  # ?????????
            full_mail = self.print_info(msg)  # ??????????????????
            att_list=self.get_att(msg, self.file_edit.text())
            full_mail+=("Attached files: "+str(att_list))
            self.body_edit.setText(full_mail)
        else:
            self.not_exist_warning.exec_()
        server.quit()

    def del_mail(self):
        email = self.sender_edit.text()
        password = self.license_edit.text()  # ?????????????????????
        pop3_server = 'pop.' + self.sender_edit.text()[self.sender_edit.text().rfind('@') + 1:]
        server = poplib.POP3_SSL(pop3_server)
        server.set_debuglevel(1)
        # print(server.getwelcome().decode('utf-8'))
        server.user(email)
        server.pass_(password)
        resp, mails, octets = server.list()
        total = len(mails)
        id = int(self.id_edit.text())
        if id < total:
            index = total - id
            server.dele(index)
        else:
            not_exist_warning = QMessageBox.warning(self,'Warning','That mail does not exist!',QMessageBox.Yes)
        server.quit()
