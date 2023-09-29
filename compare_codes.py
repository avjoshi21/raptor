import numpy as np
import sys,os,glob
import click
import matplotlib.pyplot as plt
sys.path.insert(1,'/home/avjoshi2/afd_ipole/analysis_related/utility_files/')
import notebookUtils as iutils
from mpl_toolkits.axes_grid1 import ImageGrid

def loadIpoleIm(ipoleim):
    ipoleData = iutils.plotImage(ipoleim,returnData=True)
    return ipoleData

def loadRaptorIm(raptorim):
    raptorData = np.loadtxt(raptorim)
    imsize=int(np.sqrt(raptorData.shape[0]))
    raptorData = raptorData.reshape((imsize,imsize,raptorData.shape[1]))
    return raptorData

@click.command()
@click.option('--ipoleim')
@click.option('--raptorim')
def compare_images(ipoleim,raptorim):
    ipoleData = loadIpoleIm(ipoleim)
    raptorData = loadRaptorIm(raptorim)
    stokesVector = ['I','Q','U','V']
    # fig,axs=plt.subplots(1,2);
    fig=plt.figure(figsize=(6,12))
    axs = ImageGrid(fig,111,
            nrows_ncols = (2,4),
            axes_pad = (0.5,0.1),
            cbar_location = "right",
            cbar_mode="each",
            cbar_size="5%",
            cbar_pad=0.05
            )
    for i in range(4):
      ipoleData[stokesVector[i]]*=ipoleData['scale']
      dataLims = [0.007,0.0015,0.0015,0.00025]
      vmax0=dataLims[i]
      vmax1=dataLims[i]
      if i==0:
        cmap = 'afmhot'
        vmin0=0
        vmin1=0
        #vmax0=np.max(ipoleData[stokesVector[i]])
        #vmax1=np.max(raptorData[:,:,2+i])
      else:
        cmap = 'seismic'
        #vmax0=np.max(ipoleData[stokesVector[i]])
        #vmax1=np.max(raptorData[:,:,2+i])
        vmin0=-vmax0
        vmin1=-vmax1
      axs[i].set_title(stokesVector[i])
      im0=axs[i].imshow(ipoleData[stokesVector[i]],origin='lower',cmap=cmap,vmin=vmin0,vmax=vmax0)
      im1=axs[4+i].imshow(raptorData[:,:,2+i].T,origin='lower',cmap=cmap,vmin=vmin1,vmax=vmax1)
      cb0 = plt.colorbar(im0,cax=axs.cbar_axes[i])
      cb0.ax.tick_params(labelsize=5)
      cb1 = plt.colorbar(im1,cax=axs.cbar_axes[4+i])
      cb1.ax.tick_params(labelsize=5)
      axs[i].tick_params(axis='both',bottom=False,left=False,labelbottom=False,labelleft=False)
      axs[i+4].tick_params(axis='both',left=False,bottom=False,labelbottom=False,labelleft=False)
    axs[0].set_ylabel("ipole")
    axs[4].set_ylabel("raptor")
    plt.subplots_adjust(left=0,right=1,bottom=0,top=1,wspace=0,hspace=0)
    plt.savefig("ipole_raptor_comp.png",dpi=200,bbox_inches="tight")

if __name__=="__main__":
    compare_images();
