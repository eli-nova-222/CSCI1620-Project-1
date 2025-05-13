from PyQt6.QtWidgets import *
from gui1 import *
import csv

class Logic(QMainWindow, Ui_MainWindow):

    def __init__(self):
        """
        Setup ui

        return: None
        """
        super().__init__()
        self.setupUi(self)

        #submit button command
        self.button_submit.clicked.connect(lambda: self.submit())

    def submit(self):
        """
        Records vote and id when submit button clicked

        :return: None
        """
        try:
         #check type of id input
         id_num = int(self.input_id.text().strip())
         #check vote cast
         vote = self.cast_vote()

         #check for preexisting ID
         id_reader = csv.reader(open('vote.csv'))
         for row in id_reader:
             if int(row[0]) == id_num:
                 raise UserWarning

         # writes to csv file
         with open('vote.csv', 'a+', newline='') as csvfile:
             writer = csv.writer(csvfile)
             vote_data = [id_num, vote]
             writer.writerow(vote_data)

         #reset if correct
         self.label_result.setText('VOTE SUBMITTED')
         self.input_id.setText('')

        #exception for non-int id num
        except ValueError:
            self.label_result.setText(f'ID must only use digits [0-9]')
            self.input_id.setText('')

        #exception for non-unique ID
        except UserWarning:
            self.input_id.setText('')
            self.label_result.setText(f'ID already recorded')

        # exception for no candidate selected
        except Warning:
            self.label_result.setText(f'Please select candidate')
            self.input_id.setText('')

    def cast_vote(self):
        """
        Gets the vote cast, returns the candidate selected

        :return: name of candidate (str)
        """
        #checks radio buttons
        if self.radio_bianca.isChecked():
            return 'bianca'
        elif self.radio_edward.isChecked():
            return 'ed'
        elif self.radio_felicia.isChecked():
            return 'felicia'
        else:
            raise Warning

    def closeEvent(self, event):
        """
        Creates 'final vote' window popup when main program closed

        :param event: Builtin close window event
        :return: None
        """

        b_vote = 0
        e_vote = 0
        f_vote = 0

        # reads through csv to count votes
        vote_reader = csv.reader(open('vote.csv'))
        for row in vote_reader:
            if row[1] == 'bianca':
                b_vote+=1
            elif row[1] == 'ed':
                e_vote+=1
            elif row[1] == 'felicia':
                f_vote+=1

        #creates message box and text
        vote_msg = QMessageBox()
        vote_msg.setWindowTitle("Final Vote")
        vote_msg.setText(f'Bianca - {b_vote}\n '
                         f'Edward - {e_vote}\n'
                         f'Felicia - {f_vote}')
        x = vote_msg.exec()

        event.accept()

