# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from NewImageSource import my_canny_04
from PIL import Image
import numpy as np

import argparse
import sys
import os

import numpy as np
import tensorflow as tf

main_stations = ["ard", "br", "hr", "kabel1", "livestrip", "mdr", "n24", "ndr", "prosieben", "sat1", "susilive", "swr", "wdr", "zdf"]

def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph

def read_tensor_from_image_file(file_name, input_height=299, input_width=299,
				input_mean=0, input_std=255):
  input_name = "file_reader"
  output_name = "normalized"
  file_reader = tf.read_file(file_name, input_name)
  if file_name.endswith(".png"):
    image_reader = tf.image.decode_png(file_reader, channels = 3,
                                       name='png_reader')
  elif file_name.endswith(".gif"):
    image_reader = tf.squeeze(tf.image.decode_gif(file_reader,
                                                  name='gif_reader'))
  elif file_name.endswith(".bmp"):
    image_reader = tf.image.decode_bmp(file_reader, name='bmp_reader')
  else:
    image_reader = tf.image.decode_jpeg(file_reader, channels = 3,
                                        name='jpeg_reader')
  float_caster = tf.cast(image_reader, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0);
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.Session()
  result = sess.run(normalized)

  return result

def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label

def getPrefix(s):
  for pre in main_stations:
    if s.startswith(pre):
      return pre
  return s

def predict(clf):
  best = 0.0
  predict = "no_logo"
  for k,v in clf.items():
    if v['percentage'] > best:
      best = v['percentage']
      predict = (k, best)

  return predict

def classify(files, mode):
  if __name__ == "__main__":
    model_file = "incept_fulldata/retrained_graph.pb"
    label_file = "incept_fulldata/retrained_labels.txt"
    input_height = 299
    input_width = 299
    input_mean = 128
    input_std = 128
    input_layer = "Mul"
    output_layer = "final_result"

    graph = load_graph(model_file)

    threshold = 0.5
    
    classifications = {}

    for file_name in files:
      if not file_name.endswith(".jpg") or "canny" in file_name:
        continue

      if mode == "canny":
        imgArray = np.asarray(Image.open(file_name))
        file_name = file_name[:-4] + "_canny.jpg"
        muh = Image.fromarray(np.uint8(my_canny_04(imgArray)))
        muh.save(file_name)

      print("Classify file " + file_name)
      t = read_tensor_from_image_file(file_name,
                                      input_height=input_height,
                                      input_width=input_width,
                                      input_mean=input_mean,
                                      input_std=input_std)

      input_name = "import/" + input_layer
      output_name = "import/" + output_layer

      input_operation = graph.get_operation_by_name(input_name);
      output_operation = graph.get_operation_by_name(output_name);

      with tf.Session(graph=graph) as sess:
        results = sess.run(output_operation.outputs[0], {input_operation.outputs[0]: t})
        results = np.squeeze(results)

        top_k = results.argsort()[-5:][::-1]
        labels = load_labels(label_file)
        topLabels = map(lambda i: (labels[i], results[i]), top_k)

        classification = {}

        for tl, percent in topLabels:
          prefix = getPrefix(tl)

          if not prefix == tl or not prefix in classification:
            classification[prefix] = {
              "percentage": 0.0,
              "elements": []
            }
            c = classification[prefix]
          else:
            c = classification[prefix] 

          c["elements"].append((tl, percent))
          c["percentage"] += percent

        prediction = predict(classification)
        print(prediction)
        if prediction[1] > threshold:
          classification["prediction"] = prediction
        else:
          classification["prediction"] = "no logo"
        classifications[file_name] = classification

    print(classifications)
    return classifications

if len(sys.argv) == 3:
    mode = sys.argv[2]
    print("Found command line path, starting classification on images in directory. [Mode: " + mode + "]")
    classify(map(lambda f: os.path.join(sys.argv[1], f), os.listdir(sys.argv[1])), mode)

