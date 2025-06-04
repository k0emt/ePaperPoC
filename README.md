# ePaper UI Proof of Concept

See [Notes](NOTES.md) for device, build, and resource information

![proof of concept image of VFO](images/epaper-VFO.jpg)

## System Architecture

The following diagram illustrates the relationships between the main classes in the ePaperPoC project:

```mermaid
classDiagram
    class RadioApp {
        -button_manager: ButtonStateManager
        -radio: Radio
        -display: RadioDisplay
        -command_handler: RadioCommandHandler
        +main()
        +run()
    }
    
    class Radio {
        -frequency: float
        -band: Band
        -mode: Mode
        -radio_mode: RadioMode
        -observers: list
        +set_frequency(freq)
        +set_band(band)
        +set_mode(mode)
        +add_observer(observer)
        +notify_observers()
    }
    
    class RadioDisplay {
        -radio: Radio
        -epd: EPD
        +update()
        +draw_frequency()
        +draw_band()
        +draw_mode()
    }
    
    class RadioCommandHandler {
        -radio: Radio
        +handle_button_state(state)
        +process_commands()
    }
    
    class ButtonStateManager {
        -buttons: dict
        +get_current_state()
        +is_pressed(button)
    }
    
    class ButtonState {
        +button_states: dict
        +timestamp: float
    }
    
    class EPD {
        +init()
        +clear()
        +display(image)
        +sleep()
    }
    
    class Band {
        <<enumeration>>
        BAND_80M
        BAND_40M
        BAND_20M
        BAND_15M
        BAND_10M
    }
    
    class Mode {
        <<enumeration>>
        CW
        SSB
        AM
        FM
    }
    
    class RadioMode {
        <<enumeration>>
        VFO_A
        VFO_B
        MEMORY
    }
    
    RadioApp --> ButtonStateManager : creates
    RadioApp --> Radio : creates
    RadioApp --> RadioDisplay : creates
    RadioApp --> RadioCommandHandler : creates
    
    RadioDisplay --> Radio : observes
    RadioDisplay --> EPD : uses
    RadioCommandHandler --> Radio : modifies
    ButtonStateManager --> ButtonState : produces
    Radio --> Band : uses
    Radio --> Mode : uses
    Radio --> RadioMode : uses
    
    RadioApp ..> ButtonStateManager : reads states
    RadioApp ..> RadioCommandHandler : passes ButtonState
    RadioCommandHandler ..> Radio : updates state
    Radio ..> RadioDisplay : notifies changes
    RadioDisplay ..> EPD : renders to display
```

### Key Relationships

- **RadioApp** serves as the main orchestrator, creating and coordinating all other components
- **Radio** implements the observer pattern, notifying **RadioDisplay** of state changes
- **ButtonStateManager** reads hardware button inputs and provides **ButtonState** objects
- **RadioCommandHandler** processes button combinations and updates **Radio** state
- **RadioDisplay** observes **Radio** changes and renders updates to the ePaper display via **EPD**
- The enums (**Band**, **Mode**, **RadioMode**) define the possible states for the radio

## Running the PoC

With this demo, you can use the keys:

* Key 4, VFO down
* Key 3, VFO up
* Key 1 and Key 2 simultaneously, band up
* Key 3 and Key 4 simultaneously, band down
* ALL to exit

```shell
python3 radio_app.py
```

## Screen function demos

```shell
python3 display_demo.py
```

## Fonts

You will need to obtain the [Audiowide-Regular.ttf font from Google](https://fonts.google.com/specimen/Audiowide) and place it in the fonts subdirectory.
