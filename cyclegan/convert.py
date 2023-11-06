import os
from options.conversion_options import ConversionOptions
from data import create_dataset
from models import create_model
from util.image_functions import save_image, tensor2im
from pathlib import Path
from glob import glob
import zipfile

if __name__ == '__main__':
    opt = ConversionOptions().parse()
    dataset = create_dataset(opt)
    model = create_model(opt)
    model.setup(opt)
    save_folder = opt.results_dir
    os.makedirs(save_folder,exist_ok=True)


    for i, data in enumerate(dataset):
        model.set_input(data)
        model.test()
        visuals = model.get_current_visuals()
        img_path = Path(model.get_image_paths()[0]).stem
        for label, image_tensor in visuals.items():
            if label == "real":
                continue
            img = tensor2im(image_tensor)
            image_name = '%s_%s.png' % (img_path, label)
            save_path = os.path.join(save_folder, image_name)
            save_image(img, save_path, 1)
    
    files = glob(save_folder+"*png")
    with zipfile.ZipFile(save_folder+f"{save_folder.split('/')[1]}.zip", 'w') as zipMe:        
        for file in files:
            zipMe.write(file, compress_type=zipfile.ZIP_DEFLATED)
            os.remove(file)