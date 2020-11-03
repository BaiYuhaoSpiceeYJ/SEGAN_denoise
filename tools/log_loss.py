import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

smooth = 1 #40
a = 35000//smooth #300
length = 8
height = 8

d_real_losses = []
d_feak_losses = []
g_adv_losses = []
g_l1_losses = []

num = 0
with open('log_loss.txt','r') as f:
    for line in f:
        num_new = (line.split(' ')[1]).split(')')[0]
        delta = int(num_new) - int(num)
        num = num_new
        #assert delta==50 or delta == -474950
        d_real_loss = line.split(' ')[6].split(':')[-1].split(',')[0]
        d_feak_loss = line.split(' ')[7].split(':')[-1].split(',')[0]
        g_adv_loss = line.split(' ')[8].split(':')[-1].split(',')[0]
        g_l1_loss = line.split(' ')[9].split(':')[-1].split(',')[0]
        d_real_losses.append(np.float(d_real_loss))
        d_feak_losses.append(np.float(d_feak_loss))
        g_adv_losses.append(np.float(g_adv_loss))
        g_l1_losses.append(np.float(g_l1_loss))

x = 50*np.arange(len(d_real_losses))
xnew = np.linspace(x.min(),x.max(),np.int(len(d_real_losses)/smooth))

d_real_losses_smooth = make_interp_spline(x,d_real_losses)(xnew)
d_feak_losses_smooth = make_interp_spline(x,d_feak_losses)(xnew)
g_adv_losses_smooth = make_interp_spline(x,g_adv_losses)(xnew)
g_l1_losses_smooth = make_interp_spline(x,g_l1_losses)(xnew)


plt.figure(figsize=(length, height))
plt.subplot(411).set_title('d_real_losses')
plt.plot(xnew[-a:],d_real_losses_smooth[-a:])
plt.subplot(412).set_title('d_feak_losses')
plt.plot(xnew[-a:],d_feak_losses_smooth[-a:])
plt.subplot(413).set_title('g_adv_losses')
plt.plot(xnew[-a:],g_adv_losses_smooth[-a:])
plt.subplot(414).set_title('g_l1_losses')
plt.plot(xnew[-a:],g_l1_losses_smooth[-a:])
plt.tight_layout()
plt.show()