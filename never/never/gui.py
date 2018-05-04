#!/usr/bin/env python
# coding=utf-8
from urwid import MainLoop, SolidFill, \
    ExitMainLoop, AttrMap, LineBox, \
    Overlay, Text, Edit, Button, \
    Padding, Filler, Pile, \
    Divider

colors = ['black', 'dark red',
          'dark green', 'brown',
          'dark blue', 'dark magenta',
          'dark cyan', 'light gray',
          'dark gray', 'light red',
          'light green', 'yellow',
          'light blue', 'light magenta',
          'light cyan', 'white']
simple_colours = [
    ('basic', colors[11], colors[4]),
    ('redongrey', colors[1], colors[7]),
    ('blackongrey', colors[0], colors[7]),
    ('inputfield', colors[0], colors[8]),
    ('button.normal', colors[0], colors[8]),
    ('button.focus', colors[1] + ',bold', colors[8])
]


class PasswordDialog:
    mask = '*'
    caption_text = 'Enter masterpassword:'

    def __init__(self):
        # self.caption = AttrMap(
        #         Text(
        #             ('caption', self.caption_text), align='center'
        #         ),
        #         'blackongrey'
        # )
        self.caption = Text(
                    ('caption', self.caption_text), align='center'
                )
        self.inputbox_a = Padding(
                AttrMap(
                        Edit(multiline=False, mask=self.mask),
                        'inputfield'
                ), align='center', width=24
        )
        self.divider = Padding(Divider(' '), align='center')
        self.inputbox_b = Padding(
                AttrMap(
                        Edit(multiline=False, mask=self.mask),
                        'inputfield'
                ), align='center', width=24
        )
        self.innerbox = AttrMap(
                LineBox(
                        Pile(
                                [self.inputbox_a, self.divider, self.inputbox_b])),
                'blackongrey'
        )
        # scratchpad = Text('<enter>')
        self.button = Button('OK', on_press=self._ok_button)
        self.button_wrap = Padding(
                AttrMap(
                        self.button,
                        'button.normal',
                        'button.focus'
                ),
                align='center', width=15
        )

    def compose(self):
        return Filler(
            Pile([
                self.caption,
                self.innerbox,
                # scratchpad,
                self.button_wrap]
                )
        )

    def _ok_button(self):
        raise ExitMainLoop({'pw': self.inputbox_a.ge})


def callback(key):
    if key == 'f10':
        raise ExitMainLoop


def main():
    background = AttrMap(
            SolidFill(' '), 'basic'
    )
    pwdialog = PasswordDialog().compose()
    box = AttrMap(LineBox(pwdialog), 'blackongrey')
    window = Overlay(
            box,
            background,
            'center', 30,
            'middle', 10
    )

    mainloop = MainLoop(
            window,
            unhandled_input=callback,
            palette=simple_colours
    )
    mainloop.run()


if __name__ == "__main__":
    main()
