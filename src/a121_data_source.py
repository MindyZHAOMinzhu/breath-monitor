import time
import numpy as np

# A121 SDK [https://github.com/acconeer/acconeer-python-exploration]

# import acconeer.exptool as et
# from acconeer.exptool import a121
# from acconeer.exptool.a121.algo.breathing import RefApp
# from acconeer.exptool.a121.algo.breathing._ref_app import (
#     BreathingProcessorConfig,
#     RefAppConfig,
#     get_sensor_config,
# )
# from acconeer.exptool.a121.algo.presence import ProcessorConfig as PresenceProcessorConfig


class FakeBreathingResult:
    def __init__(self):
        self.breathing_rate = np.random.normal(16, 2)
        self.amplitude = np.random.uniform(0.8, 1.2)
        self.distance = np.random.uniform(50, 70)
        self.is_breathing = True
        self.has_movement = False


class A121BreathingMonitor:
    def __init__(self, use_fake=True):
        self.use_fake = use_fake

        if not self.use_fake:
            self.sensor_id = 1
            self.breathing_processor_config = BreathingProcessorConfig(
                lowest_breathing_rate=6,
                highest_breathing_rate=60,
                time_series_length_s=10,
            )
            self.presence_config = PresenceProcessorConfig(
                intra_detection_threshold=4,
                intra_frame_time_const=0.15,
                inter_frame_fast_cutoff=20,
                inter_frame_slow_cutoff=0.2,
                inter_frame_deviation_time_const=0.5,
            )
            self.ref_app_config = RefAppConfig(
                use_presence_processor=True,
                num_distances_to_analyze=3,
                distance_determination_duration=5,
                breathing_config=self.breathing_processor_config,
                presence_config=self.presence_config,
            )

            # Setup client
            self.client = a121.Client.open()
            sensor_config = get_sensor_config(ref_app_config=self.ref_app_config)
            self.client.setup_session(sensor_config)

            self.ref_app = RefApp(
                client=self.client,
                sensor_id=self.sensor_id,
                ref_app_config=self.ref_app_config,
            )
            self.ref_app.start()

    def get_data(self):
        if self.use_fake:
            time.sleep(0.1)
            return FakeBreathingResult()
        else:
            processed_data = self.ref_app.get_next()
            result = processed_data.breathing_result
            return result

    def stop(self):
        if not self.use_fake:
            self.ref_app.stop()
            self.client.close()
