#   Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
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

from common_import import *


class ReluConfig(APIConfig):
    def __init__(self):
        super(ReluConfig, self).__init__("relu")
        self.feed_spec = {"range": [-1, 1]}
        self.api_list = {'relu': 'relu', 'relu6': 'relu6'}
        # relu belongs to activation op series which only has one variable
        # thus relu can reuse activation parameters 
        self.alias_name = "activation"


class PDRelu(PaddleAPIBenchmarkBase):
    def build_program(self, config):
        x = self.variable(name='x', shape=config.x_shape, dtype=config.x_dtype)
        out = self.layers(config.api_name, x=x)

        self.feed_vars = [x]
        self.fetch_vars = [out]
        if config.backward:
            self.append_gradients(out, [x])


class TFRelu(TensorflowAPIBenchmarkBase):
    def build_graph(self, config):
        x = self.variable(name='x', shape=config.x_shape, dtype=config.x_dtype)
        out = self.layers(config.api_name, features=x)

        self.feed_list = [x]
        self.fetch_list = [out]
        if config.backward:
            self.append_gradients(out, [x])


if __name__ == '__main__':
    test_main(PDRelu(), TFRelu(), config=ReluConfig())
