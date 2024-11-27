import numpy as np
from skfuzzy import control as ctrl
from skfuzzy import membership as mf
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

setTemp = ctrl.Antecedent(np.arange(15, 32, 0.1), 'setTemp')
insideTemp = ctrl.Antecedent(np.arange(15, 38, 0.1), 'insideTemp')
outsideTemp = ctrl.Antecedent(np.arange(-10, 40, 0.1), 'outsideTemp')
fanSpeed = ctrl.Consequent(np.arange(0, 100, 0.1), 'fanSpeed')
compressorEff = ctrl.Consequent(np.arange(0, 100, 0.1), 'compressorEff')

setTemp['very low'] = mf.trimf(setTemp.universe, [15, 18, 20])
setTemp['low'] = mf.trimf(setTemp.universe, [18, 22, 26])
setTemp['moderate'] = mf.trimf(setTemp.universe, [24, 28, 32])

insideTemp['cold'] = mf.trimf(insideTemp.universe, [15, 18, 20])
insideTemp['cool'] = mf.trimf(insideTemp.universe, [18, 22, 26])
insideTemp['comfortable'] = mf.trimf(insideTemp.universe, [24, 28, 32])
insideTemp['warm'] = mf.trimf(insideTemp.universe, [30, 34, 38])

outsideTemp['very cold'] = mf.trimf(outsideTemp.universe, [-10, 0, 10])
outsideTemp['cold'] = mf.trimf(outsideTemp.universe, [5, 15, 25])
outsideTemp['moderate'] = mf.trimf(outsideTemp.universe, [20, 30, 35])
outsideTemp['hot'] = mf.trimf(outsideTemp.universe, [34, 37, 40])

fanSpeed['stopped'] = mf.trimf(fanSpeed.universe, [0, 0, 0])
fanSpeed['low'] = mf.trimf(fanSpeed.universe, [0, 33, 66])
fanSpeed['medium'] = mf.trimf(fanSpeed.universe, [33, 66, 100])
fanSpeed['high'] = mf.trimf(fanSpeed.universe, [66, 100, 100])

compressorEff['off'] = mf.trimf(compressorEff.universe, [0, 0, 0])
compressorEff['poor'] = mf.trimf(compressorEff.universe, [0, 33, 66])
compressorEff['fair'] = mf.trimf(compressorEff.universe, [33, 66, 100])
compressorEff['good'] = mf.trimf(compressorEff.universe, [66, 100, 100])


## THE RULES
rule1 = ctrl.Rule(setTemp['very low'] & insideTemp['cold'] & outsideTemp['very cold'], (fanSpeed['stopped'], compressorEff['off']))
rule2 = ctrl.Rule(setTemp['very low'] & insideTemp['cold'] & outsideTemp['cold'], (fanSpeed['low'], compressorEff['off']))
rule3 = ctrl.Rule(setTemp['very low'] & insideTemp['cold'] & outsideTemp['moderate'], (fanSpeed['medium'], compressorEff['poor']))
rule4 = ctrl.Rule(setTemp['very low'] & insideTemp['cold'] & outsideTemp['hot'], (fanSpeed['medium'], compressorEff['poor']))
rule5 = ctrl.Rule(setTemp['very low'] & insideTemp['cool'] & outsideTemp['very cold'], (fanSpeed['low'], compressorEff['poor']))
rule6 = ctrl.Rule(setTemp['very low'] & insideTemp['cool'] & outsideTemp['cold'], (fanSpeed['low'], compressorEff['poor']))
rule7 = ctrl.Rule(setTemp['very low'] & insideTemp['cool'] & outsideTemp['hot'], (fanSpeed['high'], compressorEff['fair']))
rule8 = ctrl.Rule(setTemp['very low'] & insideTemp['comfortable'] & outsideTemp['very cold'], (fanSpeed['medium'], compressorEff['fair']))
rule9 = ctrl.Rule(setTemp['very low'] & insideTemp['comfortable'] & outsideTemp['cold'], (fanSpeed['medium'], compressorEff['good']))
rule10 = ctrl.Rule(setTemp['very low'] & insideTemp['comfortable'] & outsideTemp['moderate'], (fanSpeed['medium'], compressorEff['good']))
rule11 = ctrl.Rule(setTemp['very low'] & insideTemp['comfortable'] & outsideTemp['hot'], (fanSpeed['high'], compressorEff['good']))
rule12 = ctrl.Rule(setTemp['very low'] & insideTemp['warm'] & outsideTemp['very cold'], (fanSpeed['medium'], compressorEff['good']))
rule13 = ctrl.Rule(setTemp['very low'] & insideTemp['warm'] & outsideTemp['moderate'], (fanSpeed['high'], compressorEff['good']))
rule14 = ctrl.Rule(setTemp['very low'] & insideTemp['warm'] & outsideTemp['hot'], (fanSpeed['high'], compressorEff['good']))

rule21 = ctrl.Rule(setTemp['low'] & insideTemp['cold'] & outsideTemp['very cold'], (fanSpeed['stopped'], compressorEff['off']))
rule22 = ctrl.Rule(setTemp['low'] & insideTemp['cold'] & outsideTemp['cold'], (fanSpeed['low'], compressorEff['off']))
rule23 = ctrl.Rule(setTemp['low'] & insideTemp['cold'] & outsideTemp['moderate'], (fanSpeed['low'], compressorEff['fair']))
rule24 = ctrl.Rule(setTemp['low'] & insideTemp['cold'] & outsideTemp['hot'], (fanSpeed['medium'], compressorEff['fair']))
rule25 = ctrl.Rule(setTemp['low'] & insideTemp['cool'] & outsideTemp['very cold'], (fanSpeed['low'], compressorEff['off']))
rule26 = ctrl.Rule(setTemp['low'] & insideTemp['cool'] & outsideTemp['cold'], (fanSpeed['low'], compressorEff['poor']))
rule27 = ctrl.Rule(setTemp['low'] & insideTemp['cool'] & outsideTemp['moderate'], (fanSpeed['medium'], compressorEff['fair']))
rule28 = ctrl.Rule(setTemp['low'] & insideTemp['cool'] & outsideTemp['hot'], (fanSpeed['medium'], compressorEff['fair']))
rule29 = ctrl.Rule(setTemp['low'] & insideTemp['comfortable'] & outsideTemp['very cold'], (fanSpeed['low'], compressorEff['poor']))
rule30 = ctrl.Rule(setTemp['low'] & insideTemp['comfortable'] & outsideTemp['cold'], (fanSpeed['medium'], compressorEff['poor']))
rule31 = ctrl.Rule(setTemp['low'] & insideTemp['comfortable'] & outsideTemp['moderate'], (fanSpeed['high'], compressorEff['poor']))
rule32 = ctrl.Rule(setTemp['low'] & insideTemp['comfortable'] & outsideTemp['hot'], (fanSpeed['high'], compressorEff['fair']))
rule33 = ctrl.Rule(setTemp['low'] & insideTemp['warm'] & outsideTemp['very cold'], (fanSpeed['medium'], compressorEff['good']))
rule34 = ctrl.Rule(setTemp['low'] & insideTemp['warm'] & outsideTemp['cold'], (fanSpeed['medium'], compressorEff['good']))
rule35 = ctrl.Rule(setTemp['low'] & insideTemp['warm'] & outsideTemp['moderate'], (fanSpeed['high'], compressorEff['good']))
rule36 = ctrl.Rule(setTemp['low'] & insideTemp['warm'] & outsideTemp['hot'], (fanSpeed['high'], compressorEff['good']))

rule41 = ctrl.Rule(setTemp['moderate'] & insideTemp['cold'] & outsideTemp['very cold'], (fanSpeed['stopped'], compressorEff['off']))
rule42 = ctrl.Rule(setTemp['moderate'] & insideTemp['cold'] & outsideTemp['cold'], (fanSpeed['stopped'], compressorEff['off']))
rule43 = ctrl.Rule(setTemp['moderate'] & insideTemp['cold'] & outsideTemp['moderate'], (fanSpeed['low'], compressorEff['poor']))
rule44 = ctrl.Rule(setTemp['moderate'] & insideTemp['cold'] & outsideTemp['hot'], (fanSpeed['medium'], compressorEff['poor']))
rule45 = ctrl.Rule(setTemp['moderate'] & insideTemp['cool'] & outsideTemp['very cold'], (fanSpeed['low'], compressorEff['off']))
rule46 = ctrl.Rule(setTemp['moderate'] & insideTemp['cool'] & outsideTemp['cold'], (fanSpeed['low'], compressorEff['off']))
rule47 = ctrl.Rule(setTemp['moderate'] & insideTemp['cool'] & outsideTemp['hot'], (fanSpeed['medium'], compressorEff['fair']))
rule48 = ctrl.Rule(setTemp['moderate'] & insideTemp['comfortable'] & outsideTemp['very cold'], (fanSpeed['medium'], compressorEff['off']))
rule49 = ctrl.Rule(setTemp['moderate'] & insideTemp['comfortable'] & outsideTemp['cold'], (fanSpeed['medium'], compressorEff['off']))
rule50 = ctrl.Rule(setTemp['moderate'] & insideTemp['comfortable'] & outsideTemp['moderate'], (fanSpeed['medium'], compressorEff['poor']))
rule51 = ctrl.Rule(setTemp['moderate'] & insideTemp['warm'] & outsideTemp['very cold'], (fanSpeed['medium'], compressorEff['poor']))
rule52 = ctrl.Rule(setTemp['moderate'] & insideTemp['warm'] & outsideTemp['cold'], (fanSpeed['medium'], compressorEff['poor']))
rule53 = ctrl.Rule(setTemp['moderate'] & insideTemp['warm'] & outsideTemp['moderate'], (fanSpeed['high'], compressorEff['poor']))
rule54 = ctrl.Rule(setTemp['moderate'] & insideTemp['warm'] & outsideTemp['hot'], (fanSpeed['high'], compressorEff['fair']))

rules = [
    rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14,
    rule21, rule22, rule23, rule24, rule25, rule26, rule27, rule28, rule29, rule30, rule31, rule32, rule33, rule34, rule35, rule36,
    rule41, rule42, rule43, rule44, rule45, rule46, rule47, rule48, rule49, rule50, rule51, rule52, rule53, rule54
]

aircon_ctrl = ctrl.ControlSystem(rules=rules)
aircon = ctrl.ControlSystemSimulation(control_system=aircon_ctrl)

print("Hello. This is a fuzzy system designed to identify the optimized settings for air conditioner to converse wasted energy.")
print("Make sure your input under the range: setTemp(15 to 32), insideTemp(15 to 38), outsideTemp(-10 to 40)")
# setTempValue = int(input("Enter the Set Temperature: "))
setTempValue = 22
insideTempValue = int(input("Enter the Inside Temperature: "))
outsideTempValue = int(input("Enter the Outside Temperature: "))
print("")

# define the values for the inputs
## DO IT FOR FEW ITERATIONS TO SHOW HOW TEMPERATURE CHANGE
aircon.input['setTemp'] = setTempValue
aircon.input['insideTemp'] = insideTempValue
aircon.input['outsideTemp'] = outsideTempValue

# compute the outputs
aircon.compute()

# to extract the outputs
print("Best level of FanSpeed is " + "{:.4f}".format(aircon.output['fanSpeed']))
print("Best level of Compressor Efficiency is " + "{:.4f}".format(aircon.output['compressorEff']))
print("")
print("Results of the graphs are displayed. Close all the windows in order to proceed.")
fanSpeed.view(sim=aircon)
compressorEff.view(sim=aircon)
print("")
debug = int(input("Enter 1 if you wish check the output space of the Set Temperature, enter 0 if you wish to close everything: "))

if debug == 1:
  print("")
  print("Please wait for the 3D space to be loaded....")
  ## HAVE THREE SETS OF TWO INPUTS FOR GRAPH (ex: x1,y1,z1; x2,y2,z2; x3,y3,z3)
  x1, y1 = np.meshgrid(np.linspace(insideTemp.universe.min(), insideTemp.universe.max(), 100),
                    np.linspace(outsideTemp.universe.min(), outsideTemp.universe.max(), 100))
  z1_fanSpeed = np.zeros_like(x1, dtype=float)
  z1_compressorEff = np.zeros_like(x1, dtype=float)

  # print(x1)
  # print(y1)
  for i,r in enumerate(x1):
    for j,c in enumerate(r):
      aircon.input['setTemp'] = setTempValue
      aircon.input['insideTemp'] = x1[i,j]
      aircon.input['outsideTemp'] = y1[i,j]
      try:
        aircon.compute()
        # print("safe")
      except:
        z1_fanSpeed[i,j] = float('inf')
        z1_compressorEff[i,j] = float('inf')
        # print("not safe")
      z1_fanSpeed[i,j] = aircon.output['fanSpeed']
      z1_compressorEff[i,j] = aircon.output['compressorEff']
      # print(z1_fanSpeed[i,j])
      # print(z1_compressorEff[i,j])

  def plot3d(x, y, z): 
      fig = plt.figure()
      ax = fig.add_subplot(111, projection='3d')

      ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis', linewidth=0.4, antialiased=True)

      ax.contourf(x, y, z, zdir='z', offset=-2.5, cmap='viridis', alpha=0.5)
      ax.contourf(x, y, z, zdir='x', offset=x.max() * 1.5, cmap='viridis', alpha=0.5)
      ax.contourf(x, y, z, zdir='y', offset=y.max() * 1.5, cmap='viridis', alpha=0.5)

      ax.view_init(30, 200)


  plot3d(x1, y1, z1_fanSpeed)
  plot3d(x1, y1, z1_compressorEff)

  plt.show()

print("")  
print("The program has completed.")