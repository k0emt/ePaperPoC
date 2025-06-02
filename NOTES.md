# WaveShare 2.7" ePaper HAT notes

[Manufacturer Installation Guide](https://www.waveshare.com/wiki/2.7inch_e-Paper_HAT_Manual)

[Amazon US seller](https://www.amazon.com/2-7inch-Resolution-Two-Color-Interface-Raspberry/dp/B07PKSZ3XK?ie=UTF8)

## Configure Raspberry PI for HAT

 A Raspberry Pi 5 was used for this project.

```sh
sudo raspi-config
Choose Interfacing Options -> SPI -> Yes Enable SPI interface
# then reboot
sudo reboot
```

## Coding

When building with C `sudo make -j4 EPD=epd2in7V2`

When running the Python example `python3 epd_2in7_V2_test.py`

## Resources

[Build article](https://dev.to/ranewallin/getting-started-with-the-waveshare-2-7-epaper-hat-on-raspberry-pi-41m8)

[Code gist](https://gist.github.com/RaneWallin/fd73ddbffdabea23358f722adb9f4075)
