from __future__ import print_function, division, absolute_import

import os
import libsbml

from .MetabolicModel import MetabolicModel
from ..globals import MODEL_DIR
from . import importMATLAB
from . import importSBML2
from . import importSBML3

# ----------------------------------------
# Loading models from either XML or MATLAB outputs
# ----------------------------------------


def load_metabolic_model(model_name, species='homo_sapiens'):
    """
    Loads the metabolic model from `file_name`, returning a Model object
    """

    if model_name.endswith('_mat'):
        model = importMATLAB.load(model_name, species)
    else:
        model_dir = os.path.join(MODEL_DIR, model_name)
        model_file = [x for x in os.listdir(model_dir)
                      if x.lower().endswith('.xml') or
                         x.lower().endswith('.xml.gz')]

        if len(model_file) == 0:
            raise Exception(
                "Invalid model - could not find .xml or .xml.gz file in " +
                model_dir)
        else:
            model_file = model_file[0]

        full_path = os.path.join(model_dir, model_file)
        sbmlDocument = libsbml.readSBMLFromFile(full_path)

        level = sbmlDocument.getLevel()

        if level == 3:
            model = importSBML3.load(model_name, sbmlDocument)
        elif level == 2:
            model = importSBML2.load(model_name, sbmlDocument)
        else:
            raise Exception(
                "Invalid level {} for model {}".format(
                    level, model_file)
            )

    return model
