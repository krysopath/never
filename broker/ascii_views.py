#!/usr/bin/env python
# coding=utf-8

from asciimatics.widgets import Frame, ListBox, Layout, \
    Divider, Text, Button, TextBox, Widget, Label
from asciimatics.exceptions import NextScene, StopApplication


class ListView(Frame):
    def __init__(self, screen, model):
        super(ListView, self).__init__(
            screen,
            screen.height * 75 // 100,
            screen.width * 75 // 100,
            on_load=self._reload_list,
            hover_focus=True,
            title="Login List",
            y=1
        )
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        self._list_view = ListBox(
            Widget.FILL_FRAME,
            model.get_summary(),
            name="logins",
            on_change=self._on_pick)
        self._edit_button = Button("Edit", self._edit)
        self._delete_button = Button("Delete", self._delete)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        self.filter_selector = Text("Groupfilter:", "lgroup", on_change=self._filter_list)
        layout.add_widget(self.filter_selector)
        layout.add_widget(Divider())
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Add", self._add), 0)
        layout2.add_widget(self._edit_button, 1)
        layout2.add_widget(self._delete_button, 2)
        layout2.add_widget(Button("Quit", self._quit), 3)
        self.fix()
        self._on_pick()

    def _on_pick(self):
        self._edit_button.disabled = self._list_view.value is None
        self._delete_button.disabled = self._list_view.value is None

    def _reload_list(self):
        self._list_view.options = self._model.get_summary()
        self._model.current_id = None

    def _filter_list(self):
        if self.filter_selector.value:
            self._list_view.options = self._model.get_filter_summary(self.filter_selector.value)
            self._model.current_id = None
        else:
            self._list_view.options = self._model.get_summary()
            self._model.current_id = None

    def _add(self):
        self._model.current_id = None
        raise NextScene("Edit Login")

    def _edit(self):
        self.save()
        self._model.current_id = self.data["logins"]
        raise NextScene("Edit Login")

    def _delete(self):
        self.save()
        self._model.delete_row(self.data["logins"])
        self._reload_list()

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")


class ContactView(Frame):
    def __init__(self, screen, model):
        super(ContactView, self).__init__(
            screen,
            screen.height * 75 // 100,
            screen.width * 75 // 100,
            hover_focus=True,
            title="Login Details",
            reduce_cpu=True,
            y=1
        )
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)

        layout.add_widget(Text("Login:", "login"))
        layout.add_widget(Text("Group:", "lgroup"))
        layout.add_widget(Text("Username:", "username"))
        layout.add_widget(Text("Loginlink:", "link"))
        layout.add_widget(Text("Email address:", "email"))
        layout.add_widget(Text("Length:", "length"))
        layout.add_widget(Divider())
        layout.add_widget(TextBox(
            Widget.FILL_FRAME, "Notes:", "notes", as_string=True))
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(ContactView, self).reset()

        #raise Exception(__masterpw__)
        self.data = self._model.get_current_row()

    def _ok(self):
        self.save()
        if all([v for v in self.data.values()]):
            self._model.update_current_row(self.get_data())
            raise NextScene("Main")

    def get_data(self):
        #self.data['seed'] = PWGen(__masterpw__).get()
        return self.data

    @staticmethod
    def _cancel():
        raise NextScene("Main")


class LoginView(Frame):
    def __init__(self, screen):
        super(LoginView, self).__init__(
            screen,
            screen.height * 33 // 100,
            screen.width * 33 // 100,
            hover_focus=True,
            title="Login",
            reduce_cpu=True,
            y=1
        )

        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        self._pw1 = Text("", "mpw1")
        self._pw2 = Text("", "mpw2")
        layout.add_widget(Label('enter password'))
        layout.add_widget(self._pw1)
        layout.add_widget(Divider())
        layout.add_widget(Label('confirm password'))
        layout.add_widget(self._pw2)
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def _ok(self):
        pass

    @staticmethod
    def _cancel():
        raise StopApplication('User pressed cancel')


