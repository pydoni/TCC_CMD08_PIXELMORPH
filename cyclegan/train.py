import time
from options.train_options import TrainOptions
from data import create_dataset
from models import create_model
from glob import glob
import zipfile
import os

if __name__ == '__main__':
    opt = TrainOptions().parse()
    dataset = create_dataset(opt)
    dataset_size = len(dataset)

    model = create_model(opt)
    model.setup(opt)              
    total_iters = 0  
    save_folder = opt.checkpoints_dir + "/" + opt.name + "/"              

    for epoch in range(opt.epoch_count, opt.n_epochs + opt.n_epochs_decay + 1):

        epoch_start_time = time.time()
        iter_data_time = time.time()
        epoch_iter = 0
        model.update_learning_rate()
        for i, data in enumerate(dataset):
            iter_start_time = time.time()

            total_iters += opt.batch_size
            epoch_iter += opt.batch_size
            model.set_input(data)
            model.optimize_parameters()

            if total_iters % opt.save_latest_freq == 0:
                save_suffix = 'iter_%d' % total_iters if opt.save_by_iter else 'latest'
                model.save_networks(save_suffix)
            

            iter_data_time = time.time()
        if epoch % opt.save_epoch_freq == 0:
            model.save_networks('latest')
            model.save_networks(epoch)
    
    files = glob(save_folder+"*latest*pth")
    with zipfile.ZipFile(save_folder+f"{save_folder.split('/')[1]}.zip", 'w') as zipMe:        
        for file in files:
            zipMe.write(file, compress_type=zipfile.ZIP_DEFLATED)
            os.remove(file)
    
    
