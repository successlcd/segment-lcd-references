# Segment LCD references

451 custom segment LCDs we have built at [SuccessLCD](https://successlcd.com/), in one table. Every row comes from the production drawing: LCD type, viewing area, glass outline, operating voltage, duty and bias, frame frequency, viewing direction, temperature range, connection and rear polarizer, with a link to the product page.

Most segment LCD projects start with the same questions. What glass fits behind a 45 mm window? Will it run from 3 V? Is it still readable at −30 °C? Has someone already built something close? A list of real drawings gets you to an answer faster than a blank spec, and it gives you numbers to put in your own.

Most of these were drawn for one customer's product, so treat them as starting points rather than catalogue parts. The glass size, drive conditions and connection usually carry over to a new design; the artwork usually changes.

## What's in it

| LCD type | References |
|---|---:|
| HTN | 155 |
| VA | 123 |
| TN | 122 |
| FSTN | 27 |
| DFSTN | 14 |
| STN | 10 |

266 are positive mode and 182 negative. By connection: 292 metal pins, 86 zebra, 34 FPC and 22 heat seal. 94 are rated to operate at −30 °C or colder.

- `data/segment-lcd-references.csv`: one row per reference
- `data/segment-lcd-references.json`: the same data as JSON
- `find_lcd.py`: a small command-line filter (Python 3.8 or newer, no dependencies)

## Find something close

```
$ python find_lcd.py --min-width 40 --max-width 60 --voltage 3.0 --temp-min -20
S3398D   VA    negative     57 x 45    mm  3.0 V  1/4 duty, 1/3 bias  -20 to +70 °C  https://successlcd.com/products/s3398d/
S3543D   STN   positive     58 x 47    mm  3.0 V  1/4 duty, 1/3 bias  -20 to +70 °C  https://successlcd.com/products/s3543d/
S3622D   TN    positive     51 x 71.4  mm  2.9 V  1/4 duty, 1/3 bias  -20 to +70 °C  https://successlcd.com/products/s3622d/
S3945D   TN    positive   53.8 x 16    mm  3.0 V  1/4 duty, 1/3 bias  -20 to +70 °C  https://successlcd.com/products/s3945d/
S4067D   DFSTN positive     59 x 14.5  mm  3.0 V  1/8 duty, 1/4 bias  -30 to +80 °C  https://successlcd.com/products/s4067d/
S4324D   TN    positive     42 x 42    mm  3.0 V  1/4 duty, 1/3 bias  -20 to +70 °C  https://successlcd.com/products/s4324d/
...
15 of 451 references
```

Other filters: `--type VA`, `--negative`, `--duty 1/8`, `--connection Zebra`, `--app thermostat`. Add `--csv` to get the matching rows as a spreadsheet.

Or with pandas:

```python
import pandas as pd

df = pd.read_csv("data/segment-lcd-references.csv")
cold = df[(df.operating_temp_min_c <= -30) & (df.lcd_voltage_v <= 3.3)]
print(cold[["model", "lcd_type", "viewing_area_w_mm", "viewing_area_h_mm", "url"]])
```

## By application

The same references grouped by product, with a comparison table on each page:

- [Thermostats](https://successlcd.com/application/thermostat-lcd-display/)
- [Blood pressure monitors](https://successlcd.com/application/blood-pressure-monitor-lcd/)
- [Thermometers (clinical, food and probe)](https://successlcd.com/application/thermometer-lcd-display/)
- [Thermo-hygrometers and weather stations](https://successlcd.com/application/thermo-hygrometer-lcd/)
- [Motorcycle, e-bike and vehicle instruments](https://successlcd.com/application/motorcycle-instrument-lcd/)
- [Tire pressure gauges and TPMS](https://successlcd.com/application/tire-pressure-gauge-lcd/)
- [Massagers and personal care](https://successlcd.com/application/massager-lcd-display/)
- [Dog training remotes](https://successlcd.com/application/dog-training-collar-lcd/)
- [Power supplies, chargers and power stations](https://successlcd.com/application/power-supply-lcd/)
- [Electricity, gas and fuel meters](https://successlcd.com/application/meter-lcd-display/)
- [Measuring instruments](https://successlcd.com/application/measuring-instrument-lcd/)
- [Clocks and timers](https://successlcd.com/application/clock-timer-lcd/)
- [Home appliances and smart home](https://successlcd.com/application/home-appliance-lcd-display/)

## Columns

| Column | Meaning |
|---|---|
| `model` | Our reference number |
| `url` | Product page with the full drawing data |
| `lcd_type` | TN, HTN, STN, FSTN, DFSTN or VA |
| `polarity` | `positive` (dark segments on a light background) or `negative` (light segments on a dark background, normally backlit) |
| `application` | The product the glass was designed for |
| `viewing_area_w_mm`, `viewing_area_h_mm` | Minimum viewing area from the drawing |
| `glass_outline_w_mm`, `glass_outline_h_mm` | Overall glass size, where the drawing gives it |
| `lcd_voltage_v` | LCD operating voltage (Vop) |
| `duty`, `bias` | Multiplex drive, for example 1/4 duty and 1/3 bias; `static` for direct drive |
| `frame_frequency_hz` | Frame frequency on the drawing |
| `viewing_direction` | Best viewing direction, for example 6 o'clock |
| `operating_temp_min_c`, `operating_temp_max_c` | Operating temperature range |
| `storage_temp_min_c`, `storage_temp_max_c` | Storage temperature range |
| `connection` | Metal pins, Zebra, FPC or Heat seal |
| `pin_pitch_mm` | Pin or contact pitch |
| `rear_polarizer` | `reflective`, `transflective` or `transmissive` |

An empty cell means the drawing doesn't state that value.

## Worth checking on any segment LCD drawing

**Voltage, duty and bias belong together.** The glass is tuned for good contrast at that operating voltage with that duty and bias. Drive a 1/4-duty glass at 1/8 duty and the off segments start to show, or the on segments go faint. If your driver or MCU only supports certain duty and bias settings, filter on those first.

**The temperature range is where contrast is specified.** Liquid crystal gets slow in the cold and its contrast shifts with temperature, so a glass rated −30 °C to +80 °C usually uses a different mixture from one rated 0 to +50 °C. Over a wide range, plan on adjusting the drive voltage with temperature in your driver or firmware.

**The rear polarizer decides how the display is lit.** Reflective is brightest without a backlight but can't be backlit. Transflective works with or without one. Transmissive needs the backlight on to be read, which is why negative-mode glass is almost always transmissive.

**The viewing area is a minimum.** Keep the window in your housing inside it, with room for assembly tolerance, or the edge of the seal will show.

**Viewing direction follows how the product is mounted.** It is the side the display looks best from, so work out where the user's eye sits relative to the glass before you fix it. Our [viewing direction guide](https://successlcd.com/lcd-viewing-direction/) has examples.

**The connection shapes the housing as much as the PCB.** Metal pins solder straight into the board. Zebra strips need a frame to press the glass onto pads on the PCB. FPC and heat seal let the glass sit away from the board or in a thin stack.

More background: [TN, HTN, STN, FSTN, DFSTN and VA compared](https://successlcd.com/monochrome-lcd-types/), [duty and bias explained](https://successlcd.com/segment-lcd-duty-bias/), [transflective and reflective LCDs](https://successlcd.com/transflective-lcd-display/).

## Updates and questions

The table follows the product pages on successlcd.com, and we add to it when new references go up. If a value looks wrong, open an issue and we'll check it against the drawing.

If you have artwork or a rough sketch for a new display, send it with the row that comes closest and we'll come back with what would need to change: [successlcd.com/contact](https://successlcd.com/contact/).

## License

Data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Please credit "SuccessLCD segment LCD references" with a link to this repository. Code: MIT. See [LICENSE](LICENSE).
