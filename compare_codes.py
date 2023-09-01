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

    # fig,axs=plt.subplots(1,2);
    fig=plt.figure()
    axs = ImageGrid(fig,111,
            nrows_ncols = (2,1),
            axes_pad = 0.1,
            cbar_location = "right",
            cbar_mode="each",
            cbar_size="5%",
            cbar_pad=0.05
            )
    im0=axs[0].imshow(ipoleData['I'],origin='lower',cmap='afmhot')
    im1=axs[1].imshow(raptorData[:,:,2].T,origin='lower',cmap='afmhot')
    plt.colorbar(im0,cax=axs.cbar_axes[0])
    plt.colorbar(im1,cax=axs.cbar_axes[1])
    plt.subplots_adjust(left=0,right=1,bottom=0,top=1,wspace=0,hspace=0)
    plt.savefig("ipole_raptor_comp.png",dpi=200,bbox_inches="tight")

if __name__=="__main__":
    compare_images();