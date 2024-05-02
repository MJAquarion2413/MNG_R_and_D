import dropbot_core

def main():
    controller = dropbot_core.DropbotController()
    try:
        # Run the controller in a separate thread or as a subprocess
        while True:
            cmd = input("Enter command (voltage, frequency, hv, quit): ")
            if cmd == 'quit':
                break
            elif cmd.startswith('voltage '):
                voltage = int(cmd.split()[1])
                controller.set_voltage(voltage)
            elif cmd.startswith('frequency '):
                frequency = int(cmd.split()[1])
                controller.set_frequency(frequency)
            elif cmd.startswith('hv '):
                state = cmd.split()[1].lower() == 'on'
                controller.set_hv(state)
    except KeyboardInterrupt:
        pass
    finally:
        controller.loop.stop()

if __name__ == "__main__":
    main()
