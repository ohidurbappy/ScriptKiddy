var digitOptions = [
    {text: '0 Black', index: 0, value: 0},
    {text: '1 Brown', index: 1, value: 1},
    {text: '2 Red', index: 2, value: 2},
    {text: '3 Orange', index: 3, value: 3},
    {text: '4 Yellow', index: 4, value: 4},
    {text: '5 Green', index: 5, value: 5},
    {text: '6 Blue', index: 6, value: 6},
    {text: '7 Violet', index: 7, value: 7},
    {text: '8 Grey', index: 8, value: 8},
    {text: '9 White', index: 9, value: 9}
  ];
  var multiplierOptions = [
    {text: '1Ω Black', index: 0, value: 1e0},
    {text: '10Ω Brown', index: 1, value: 1e1},
    {text: '100Ω Red', index: 2, value: 1e2},
    {text: '1KΩ Orange', index: 3, value: 1e3},
    {text: '10KΩ Yellow', index: 4, value: 1e4},
    {text: '100KΩ Green', index: 5, value: 1e5},
    {text: '1MΩ Blue', index: 6, value: 1e6},
    {text: '10MΩ Violet', index: 7, value: 1e7},
    {text: '0.1Ω Gold', index: 10, value: 1e-1},
    {text: '0.01Ω Silver', index: 11, value: 1e-2}
  ];
  var toleranceOptions = [
    {text: '±1% Brown', index: 1, value: 0.01},
    {text: '±2% Red', index: 2, value: 0.02},
    {text: '±0.5% Green', index: 5, value: 0.005},
    {text: '±0.25% Blue', index: 6, value: 0.0025},
    {text: '±0.10% Violet', index: 7, value: 0.001},
    {text: '±0.05% Grey', index: 8, value: 0.0005},
    {text: '±5% Gold', index: 10, value: 0.05},
    {text: '±10% Silver', index: 11, value: 0.1}
  ];
  var Band = function(options) {
    var options = options || {};
    if (options.multiplier) {
      this.options = multiplierOptions;
    } else if (options.tolerance) {
      this.options = toleranceOptions;
    } else {
      this.options = digitOptions;
    }
    var value = _.find(this.options, function(option) {
      return option.index == options.value;
    });
    this.value = ko.observable(value || this.options[0]);
  }
  var ViewModel = function() {
    var self = this;
    this.bands = ko.observableArray([
      new Band({value: 0}),
      new Band({value: 1}),
      new Band({value: 3, multiplier: true}),
      new Band({value: 10, tolerance: true})
    ]);


    var getBandValue = function(bandIndex) {
      return self.bands()[bandIndex].value().value;
    }
    
    var getOhmString = function(ohms) {
      var suffix = 'Ω'
      if (ohms/1e6 >= 1) {
        suffix = 'MΩ';
        ohms = ohms/1e6;
      }else if (ohms/1e3 >= 1) {
        suffix = 'KΩ';
        ohms = ohms/1e3;
      }
      return ohms + suffix;
    }
    this.calculateResistance = ko.computed(function() {
      var ohms = (getBandValue(0)*10 + getBandValue(1)) * getBandValue(2)
      return getOhmString(ohms) + ' ±' + getBandValue(3)*100 + '%';
    }, this);
  }
  ko.applyBindings(new ViewModel);