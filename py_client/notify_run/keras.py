from keras.callbacks import Callback
from _thread import start_new_thread

from notify_run import Notify


class NotifyCallback(Callback):
    def __init__(self, notify=None, action=None):
        if notify is None:
            notify = Notify()
        self.notify = notify
        self._format_pair = '{}: {:.5f}'
        self.action = action
    
    def _format_stats(self, logs):
        return ''.join(self._format_pair.format(k, v) for k, v in logs.items())

    def send_message(self, message):
        start_new_thread(self.notify.send, (message, self.action))
    
    def on_train_begin(self, logs=None):
        self.epochs = self.params['epochs']

    def on_epoch_end(self, epoch, logs=None):
        epoch += 1
        if epoch == self.epochs:
            message = 'Done training {}'.format(self.epochs)
        else:
            message = 'Done epoch {} of {}.'.format(epoch, self.epochs)
        message += ' ' + self._format_stats(logs) if logs else ''
        self.send_message(message)

