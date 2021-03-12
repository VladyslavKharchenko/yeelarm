import yeelight
from datetime import datetime as dt
from datetime import timedelta
import time
import logging
import sys

SMOOTHNESS = 891  # in seconds. 15 minutes by default


def remove_seconds(_time):
    return _time.replace(second=0, microsecond=0)


def set_alarm():
    while True:
        alarm_time = input('At what time do you want me to wake you up? ')
        try:
            alarm_time_dt = dt.strptime(alarm_time, '%H:%M')
        except ValueError as e:
            logging.error(f'{str(e)}. The time needs to be set as HOUR:MINUTE\n')
            continue

        now_time_dt = remove_seconds(dt.now().time())
        process_start_time_dt = (alarm_time_dt - timedelta(seconds=SMOOTHNESS)).time()

        if ((now_time_dt <= alarm_time_dt.time()) and
                (now_time_dt > process_start_time_dt)):

            logging.error(f'Alarm should be set at least to {SMOOTHNESS} seconds later than current time, '
                          f'e.g. {(remove_seconds(dt.now()) + timedelta(seconds=SMOOTHNESS)).time()}')
        else:
            logging.info(f'Alarm has been set to {alarm_time_dt.time()}. '
                         f'The script will start gradually increase the brightness at '
                         f'{(alarm_time_dt - timedelta(seconds=SMOOTHNESS)).time()}')
            return alarm_time_dt


def get_bulb():

    def get_parameters(bulb_dict):
        capabilities = bulb_dict.get('capabilities')
        return \
            bulb_dict.get('ip'), \
            bulb_dict.get('port'), \
            capabilities.get('model'), \
            capabilities.get('name'), \
            capabilities.get('power')

    bulbs_discovered = yeelight.discover_bulbs()
    log_message = 'ip = {0}, port = {1}, model = {2}, name = {3}, power = {4}'

    if len(bulbs_discovered) == 1:
        ip, port, model, name, power = get_parameters(bulbs_discovered.pop())
        logging.info('One bulb found, proceeding: ' + log_message.format(ip, port, model, name, power))

        return yeelight.Bulb(ip)

    elif len(bulbs_discovered) == 0:
        raise Exception(
            'No bulbs found nearby. '
            'Make sure you\'re running the script using the same local network your bulb connected to.'
        )
    else:  # more than one bulb found
        bulbs_found_msg = ''
        for index, bulb in enumerate(bulbs_discovered):
            ip, port, model, name, power = get_parameters(bulb)
            bulbs_found_msg += f'\t#{index}:\t\t{log_message.format(ip, port, model, name, power)}\n'

        logging.info(f'More than one bulb found:\n {bulbs_found_msg}')
        while True:
            try:
                chosen_index = int(
                    input('Please input the # of the bulb you want to use '
                          f'(0-{len(bulbs_discovered) - 1}): ')
                )
            except ValueError:
                logging.error('Input must be an integer!\n')
                continue
            if chosen_index in range(len(bulbs_discovered)):
                ip, port, model, name, power = get_parameters(bulbs_discovered[chosen_index])
                logging.info('Proceeding: ' + log_message.format(ip, port, model, name, power))

                return yeelight.Bulb(ip)
            else:
                logging.error(f'The bulb # should be in range [0-{len(bulbs_discovered) - 1}]\n')


def wait_for_alarm(alarm_time_dt):
    start_wake_up_time_dt = (alarm_time_dt - timedelta(seconds=SMOOTHNESS)).time()

    while True:
        now_time_dt = (remove_seconds(dt.now()) + timedelta(seconds=start_wake_up_time_dt.second)).time() # sync seconds
        if now_time_dt != start_wake_up_time_dt:
            logging.info('{0} is not equals {1}'.format(now_time_dt, start_wake_up_time_dt))
            time.sleep(60)
        else:
            logging.info('{0} is equals {1}. Time to wake up!'.format(now_time_dt, start_wake_up_time_dt))
            return


def wake_up(bulb):  # increase brightness gradually

    def sunrise_gradually(bulb, brightness):
        if brightness == 1:
            rgb = (255, 0, 0)
            bulb.set_rgb(*rgb)
        elif brightness == 21:
            rgb = (255, 77, 0)
            bulb.set_rgb(*rgb)
        elif brightness == 41:
            rgb = (255, 103, 0)
            bulb.set_rgb(*rgb)
        elif brightness == 61:
            rgb = (255, 129, 0)
            bulb.set_rgb(*rgb)
        elif brightness == 81:
            rgb = (255, 167, 0)
            bulb.set_rgb(*rgb)
        else:
            rgb = None

        if rgb is not None:
            logging.info(rgb_message.format(rgb))

    rgb_message = 'Set RGB to {}'

    # bulb.ensure_on()
    if bulb.get_properties()['power'] == 'off':
        bulb.turn_on()

    for brightness in range(1, 101):
        bulb.set_brightness(brightness)
        logging.info('Set brightness to {}'.format(brightness))

        sunrise_gradually(bulb, brightness)

        time.sleep(SMOOTHNESS/100)  # by default it's 15 minutes in summary


logging.basicConfig(
        stream=sys.stdout,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )


if __name__ == '__main__':
    bulb = get_bulb()
    alarm_time = set_alarm()
    wait_for_alarm(alarm_time)
    wake_up(bulb)
