"""Reproduce the charts and numbers in ml/random_forest_and_gbt.md.

Requires: scikit-learn==1.5.2, numpy, matplotlib.
Run from the repo root: python3 scripts/ml_figures.py
"""
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, RandomForestClassifier, GradientBoostingClassifier
from sklearn.datasets import make_friedman1, make_moons
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, log_loss
OUT='ml/img/'
BLUE,ORANGE,AQUA='#2a78d6','#eb6834','#1baf7a'; SURF='#fcfcfb'; INK='#0b0b0b'; INK2='#52514e'; GRID='#e4e3df'
plt.rcParams.update({'figure.facecolor':SURF,'axes.facecolor':SURF,'axes.edgecolor':GRID,'axes.labelcolor':INK2,
 'xtick.color':INK2,'ytick.color':INK2,'text.color':INK,'axes.grid':True,'grid.color':GRID,'grid.linewidth':0.8,
 'axes.spines.top':False,'axes.spines.right':False,'font.size':10,'lines.linewidth':2,'legend.frameon':False})
rng=np.random.RandomState(0)
# 1D fits
X=np.sort(rng.uniform(0,6,80))[:,None]; y=np.sin(X[:,0])*10+rng.normal(0,2,80)
grid=np.linspace(-1,8,600)[:,None]
models=[('One tree, max_depth=2',DecisionTreeRegressor(max_depth=2,random_state=0)),
        ('One tree, no depth limit',DecisionTreeRegressor(random_state=0)),
        ('Random forest, 300 trees',RandomForestRegressor(300,random_state=0)),
        ('Gradient boosting, 300 trees',GradientBoostingRegressor(n_estimators=300,learning_rate=0.05,max_depth=2,random_state=0))]
fig,axs=plt.subplots(2,2,figsize=(10,6.4),sharex=True,sharey=True)
for ax,(name,m) in zip(axs.flat,models):
    m.fit(X,y); ax.scatter(X[:,0],y,s=14,color='#a3a29c',zorder=2,label='training data')
    ax.plot(grid[:,0],m.predict(grid),color=BLUE,zorder=3,label='model prediction')
    ax.axvspan(-1,0,color='#efeee9',zorder=0); ax.axvspan(6,8,color='#efeee9',zorder=0)
    ax.set_title(name,fontsize=11,loc='left')
axs[0,0].legend(loc='lower left',fontsize=9)
for ax in axs[1]: ax.set_xlabel('x  (shaded = outside the training range)')
for ax in axs[:,0]: ax.set_ylabel('y')
fig.suptitle('Same 80 noisy points from y = 10 sin(x), four tree models',x=0.01,ha='left',fontsize=12)
fig.tight_layout(); fig.savefig(OUT+'fits_1d.png',dpi=150); plt.close()
# regression benchmark
Xf,yf=make_friedman1(n_samples=600,noise=2.0,random_state=1)
Xtr,Xte,ytr,yte=train_test_split(Xf,yf,test_size=0.5,random_state=1)
print('var test',yte.var())
depths=range(1,16); tr=[];te=[]
for d in depths:
    m=DecisionTreeRegressor(max_depth=d,random_state=0).fit(Xtr,ytr)
    tr.append(mean_squared_error(ytr,m.predict(Xtr))); te.append(mean_squared_error(yte,m.predict(Xte)))
print('depth', [(d,round(a,2),round(b,2)) for d,a,b in zip(depths,tr,te)])
fig,ax=plt.subplots(figsize=(7,4))
ax.plot(list(depths),tr,color=BLUE,marker='o',ms=4,label='training error'); ax.plot(list(depths),te,color=ORANGE,marker='o',ms=4,label='test error')
best=int(np.argmin(te)); ax.annotate('best test error\n(depth %d)'%(best+1),(best+1,te[best]),xytext=(best+2.5,te[best]-6),color=INK2,arrowprops=dict(arrowstyle='-',color=INK2))
ax.set_xlabel('max_depth of a single tree'); ax.set_ylabel('mean squared error'); ax.legend(); ax.set_ylim(bottom=0)
ax.set_title('One decision tree: deeper fits training data better, test data worse past a point',loc='left',fontsize=11)
fig.tight_layout(); fig.savefig(OUT+'tree_depth.png',dpi=150); plt.close()
ns=[1,2,5,10,20,50,100,200,400]; te_rf=[];oob=[]
for n in ns:
    m=RandomForestRegressor(n,random_state=0,oob_score=n>=20,bootstrap=True).fit(Xtr,ytr)
    te_rf.append(mean_squared_error(yte,m.predict(Xte)))
    oob.append(mean_squared_error(ytr,m.oob_prediction_) if n>=20 else np.nan)
print('rf', [(n,round(a,2),None if np.isnan(b) else round(b,2)) for n,a,b in zip(ns,te_rf,oob)])
fig,ax=plt.subplots(figsize=(7,4))
ax.plot(ns,te_rf,color=ORANGE,marker='o',ms=4,label='test error')
ax.plot(ns,oob,color=AQUA,marker='o',ms=4,label='out-of-bag error (no test set needed)')
ax.axhline(te[best],color=INK2,lw=1,ls='--'); ax.text(ns[-1],te[best]+0.4,'best single tree',ha='right',color=INK2,fontsize=9)
ax.set_xscale('log'); ax.set_xlabel('number of trees (log scale)'); ax.set_ylabel('mean squared error'); ax.legend(); ax.set_ylim(bottom=0)
ax.set_title('Random forest: more trees never hurts, it just stops helping',loc='left',fontsize=11)
fig.tight_layout(); fig.savefig(OUT+'rf_trees.png',dpi=150); plt.close()
# GBT rounds
for lr,depth in ((0.1,3),(0.5,3)):
    m=GradientBoostingRegressor(n_estimators=1000,learning_rate=lr,max_depth=depth,random_state=0).fit(Xtr,ytr)
    trs=[mean_squared_error(ytr,p) for p in m.staged_predict(Xtr)]; tes=[mean_squared_error(yte,p) for p in m.staged_predict(Xte)]
    b=int(np.argmin(tes)); print('gbt lr',lr,'best round',b+1,'test',round(tes[b],3),'at1000',round(tes[-1],3),'train1000',round(trs[-1],4),'r10',round(tes[9],2),'r50',round(tes[49],2))
    if lr==0.1: g=(trs,tes,b)
    else: g5=(trs,tes,b)
fig,ax=plt.subplots(figsize=(7,4))
r=np.arange(1,1001)
ax.plot(r,g[0],color=BLUE,label='training error'); ax.plot(r,g[1],color=ORANGE,label='test error')
ax.axvline(g[2]+1,color=INK2,lw=1,ls='--'); ax.text(g[2]+15,max(g[1])*0.6,'early stopping\nwould stop here\n(round %d)'%(g[2]+1),color=INK2,fontsize=9)
ax.set_xscale('log'); ax.set_xlabel('boosting round = number of trees (log scale)'); ax.set_ylabel('mean squared error'); ax.legend(); ax.set_ylim(bottom=0)
ax.set_title('Gradient boosting (learning_rate=0.1, max_depth=3): test error bottoms out, then creeps up',loc='left',fontsize=11)
fig.tight_layout(); fig.savefig(OUT+'gbt_rounds.png',dpi=150); plt.close()
rf=RandomForestRegressor(400,random_state=0).fit(Xtr,ytr); print('rf400',mean_squared_error(yte,rf.predict(Xte)))
gb=GradientBoostingRegressor(n_estimators=g[2]+1,learning_rate=0.1,max_depth=3,random_state=0).fit(Xtr,ytr); print('gb best',mean_squared_error(yte,gb.predict(Xte)))
# moons boundaries
Xm,ym=make_moons(400,noise=0.3,random_state=2)
Xmtr,Xmte,ymtr,ymte=train_test_split(Xm,ym,test_size=0.5,random_state=2)
xx,yy=np.meshgrid(np.linspace(-2,3,300),np.linspace(-1.5,2,300))
cls=[('One tree (no depth limit)',DecisionTreeClassifier(random_state=0)),('Random forest (300 trees)',RandomForestClassifier(300,random_state=0)),
     ('Gradient boosting (200 trees, depth 2)',GradientBoostingClassifier(n_estimators=200,learning_rate=0.1,max_depth=2,random_state=0))]
from matplotlib.colors import LinearSegmentedColormap
cmap=LinearSegmentedColormap.from_list('b',['#fcfcfb','#a9c8ef'])
fig,axs=plt.subplots(1,3,figsize=(12,4),sharey=True)
for ax,(name,m) in zip(axs,cls):
    m.fit(Xmtr,ymtr); P=m.predict_proba(np.c_[xx.ravel(),yy.ravel()])[:,1].reshape(xx.shape)
    acc=(m.predict(Xmte)==ymte).mean(); ll=log_loss(ymte,np.clip(m.predict_proba(Xmte),1e-15,1))
    print('moons',name,'acc',acc,'logloss',round(ll,3))
    ax.contourf(xx,yy,P,levels=np.linspace(0,1,11),cmap=cmap)
    ax.contour(xx,yy,P,levels=[0.5],colors=INK2,linewidths=1)
    ax.scatter(*Xmtr[ymtr==0].T,s=12,color=ORANGE,edgecolor=SURF,lw=0.5,label='class 0')
    ax.scatter(*Xmtr[ymtr==1].T,s=12,color='#1b4f8f',edgecolor=SURF,lw=0.5,label='class 1')
    ax.set_title('%s\ntest accuracy %.0f%%'%(name,acc*100),loc='left',fontsize=10); ax.grid(False)
axs[0].legend(loc='lower left',fontsize=9)
fig.suptitle('Predicted probability of class 1 (darker shading = higher); gray line = 50%',x=0.01,ha='left',fontsize=11)
fig.tight_layout(); fig.savefig(OUT+'boundaries.png',dpi=150); plt.close()
