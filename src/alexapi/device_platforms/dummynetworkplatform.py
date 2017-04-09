import logging
import threading
import socket
import sys
import time

from .baseplatform import BasePlatform

logger = logging.getLogger(__name__)

class DummynetworkPlatform(BasePlatform):

	def __init__(self, config):
		super(DummynetworkPlatform, self).__init__(config, 'dummynetwork')

                self.host_IP = self._pconfig['host_IP']
                self.host_port = self._pconfig['host_port']
                self.client_IP = self._pconfig['client_IP']
                
		self.trigger_thread = None
		self.started= 0

	def setup(self):
		pass

	def indicate_failure(self):
		logger.debug("setup_failure")

	def indicate_success(self):
		logger.debug("setup_complete")

	def indicate_recording(self, state=True):
		logger.debug("indicate_recording_on %s", state)

	def indicate_playback(self, state=True):
		logger.debug("indicate_playback %s", state)

	def indicate_processing(self, state=True):
		logger.debug("indicate_processing %s", state)

	def after_setup(self, trigger_callback=None):
		self._trigger_callback = trigger_callback

		if self._trigger_callback:
			self.trigger_thread = SocketServerTriggerThread(self, trigger_callback, self.host_IP, self.host_port, self.client_IP)
			self.trigger_thread.setDaemon(True)
			self.trigger_thread.start()

	def force_recording(self):
		return True

	def cleanup(self):
                self.trigger_thread.stop()



class SocketServerTriggerThread(threading.Thread):
        
        def __init__(self, platform, trigger_callback, host_IP, host_port, client_IP):
                threading.Thread.__init__(self)

                self.platform = platform
                self._trigger_callback = trigger_callback
                self.host_IP = host_IP
                self.host_port = host_port
                self.client_IP = client_IP
                self.should_run = True

        def stop(self):
                self.should_run = False

        def run(self):
                client_port = 0
                while self.should_run:
                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

                        try:
                                s.bind((self.host_IP, self.host_port))
                        except socket.error as message:
                                print 'Bind failed. Error code: %s Message %s' % (message[0], (message[1]))
                                sys.exit()

                        while 1:
                                message, address = s.recvfrom(1024)
                                if self.client_IP == address[0] and client_port != address[1]:
                                        client_port = address[1]
                                        self.platform.started = time.time()
                                        if self._trigger_callback:
                                                logger.debug('Dash Button Pushed')
                                                self._trigger_callback(self.platform.force_recording)
        

