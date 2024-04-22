__version__ = '0.17.1'
git_version = '4fd856bfbcf59a4da3a91f0e12515c7ef0709777'
from torchvision.extension import _check_cuda_version
if _check_cuda_version() > 0:
    cuda = _check_cuda_version()
