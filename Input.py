import ipywidgets as widgets
import sys, os
import traceback
from IPython.display import display
import copy


class Input:

    def __init__(self, inputType, dataType, graph, options,title):
        """

        :param inputType: on of these values: "radio", "checkboxGroup"
        :param dataType: can either be "discrimination", "corpusNames" or "analysisFunction"
                        this will be used by the models to know what kind of control is handled by this input
        :param graph:   graph to update when this input is updated
        :param options: can either be a list or a dictionary
                        - a list if you want the data displayed for the user to be directly sent to the model
                        - a dict if you want to your own words on something and translate it before sending it to
                          the model. {click here to select SwitchBoard: SWBD, click here to select mTx: MTX }

        :param title: title to be given to the input
        """

        # checking the types
        try:
            if not isinstance(inputType, str):
                message = "expected string as inputType, got " + str(type(inputType))
                raise TypeError(message)
            if not (isinstance(options, list) or isinstance(options, dict)):
                message = "expected array or dict as options, got " + str(type(options))
                raise TypeError(message)
            for item in options:
                if not isinstance(item, str):
                    message = "expected strings inside options, got " + str(type(item))
                    raise TypeError(message)
        except TypeError:
            traceback.print_exc()

        self.__optionToProgramMeaning = None
        inputOptions = None
        if isinstance(options, list):
            inputOptions = options
        else :
            inputOptions = [command for command in options]
            self.__optionToProgramMeaning = options

        if inputType == "radio":
            self.__widget = widgets.RadioButtons(
                options=inputOptions,
                value=inputOptions[0],
                description=title,
                disabled=False
            )
        elif inputType == "checkboxGroup":

            inputs = []
            for option in inputOptions:
                temp = widgets.Checkbox(
                    value=True,
                    description=option
                )
                inputs.append(temp)
            verticalBox = widgets.VBox()
            verticalBox.children = inputs
            self.__widget = verticalBox
        if inputType == "checkboxGroup":
            for widget in self.__widget.children:
                widget.observe(self._callOnChange)
        else:
            self.__widget.observe(self._callOnChange)
        self.__onChanges = None
        self.__dataType = dataType
        self.graph = graph


# --------------------------------------------------------------------------------------------------------

    def observe(self, function):
        """

        :param function: function to call when the input changes
        :return:
        """
        try:
            if not callable(function):
                message = "expected a function, got " + str(type(function))
                raise TypeError(message)
        except TypeError:
            traceback.print_exc()
        function()
        self.__onChanges = function

    def displayInput(self):
        display(self.__widget)

# --------------------------------------------------------------------------------------------------------

    def _callOnChange(self, change):
        """
        will be called when the widget changes
        :param widget: parameter given by the function from ipywidgets observe, the parameter allow us to
            know what is tthe new value of the changed widget
        :return:
        """

        try:
            if self.__onChanges is None:
                message = "onChanges function is not initialiazed"
                raise TypeError(message)
        except TypeError as e:
            print(e)
        # we have to limit onChange to only one activation by because ipywidget.observe trigger multiple time

        if change['type'] == 'change' and change['name'] == 'value':
            self.__onChanges()
            self.graph.update()

    def getDataType(self):
        return copy.copy(self.__dataType)

    def getValue(self):
        if not isinstance(self.__widget, widgets.VBox):
            if self.__optionToProgramMeaning is not None:
                value = self.__widget.value
                if value not in self.__optionToProgramMeaning:
                    print("can't link input text to something")
                    sys.exit("fatal error : input.py in getValue")
                return self.__optionToProgramMeaning[value]
            return self.__widget.value

        result = []
        for widget in self.__widget.children:
            if widget.value:
                if self.__optionToProgramMeaning is not None:
                    chosenInput = widget.description
                    if chosenInput not in self.__optionToProgramMeaning:
                        print("can't link input text to something")
                        continue
                    result.append(self.__optionToProgramMeaning[chosenInput])

                else:
                    result.append(widget.description)

        return result

    def getWidget(self):
        return self.__widget




