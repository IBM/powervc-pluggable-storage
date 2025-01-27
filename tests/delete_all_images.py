#Copyright IBM Corp. 2018.
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#http://www.apache.org/licenses/LICENSE-2.0
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.


from rest_framework import svt_tester_base
from rest_framework import novaUtils
from rest_framework import glanceUtils
from rest_framework.restUtils import HttpError
from tests import Utils

class SvtDeleteServers(svt_tester_base.SvtTesterBase):
    def test_1001_delete_images_shil(self):
        try:
            authTokenId = self.authent_id

            print('Obtaining the Image List...')
            image_list = []
            glanceUrl = self.getServiceUrl('image')
            _, img_list = glanceUtils.listImages(self.glanceUrl, authTokenId)
            to_be_deleted = []
            image_list = []
            if img_list:
                imageList = img_list['images']
            if imageList:
                for img in imageList:
                    to_be_deleted.append(img)

            if to_be_deleted:
                for image in to_be_deleted:
                    print('name=', image['name'], 'id=', image['id'])
                    image_list.append({'name': image['name'],
                                'id': image['id']})
            print('The number of images in the imagelist is %d' % len(image_list))

            get_deleted_image_list(authTokenId, self.glanceUrl, image_list)
        except HttpError as e:
            print('HTTP Error: {0}'.format(e.body))
            exit(1)

def get_deleted_image_list(authTokenId, glanceUrl, image_list):
    try:
        for image in image_list:
            print('Deleting image:name=', image['name'], 'id=', image['id'])
            deleteResponse, imageBody = \
                glanceUtils.deleteImage(glanceUrl, authTokenId, image['id'])
            print('delete http response =', deleteResponse)
            print('delete response=', imageBody)

    except HttpError as e:
        print('HTTP Error: {0}'.format(e.body))
        exit(1)

if __name__ == '__main__':
    svt_tester_base.main()
