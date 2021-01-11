import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import FileUpload from '@/components/FileUpload.vue'

const localVue = createLocalVue()

localVue.use(Vuex)

describe('FileUpload.vue', () => {
  let store
  let actions
  beforeEach(() => {
    actions = {
      upload: jest.fn()
    }
    store = new Vuex.Store({
      state: {
        upload: {
          status: '',
          error: null
        }
      },
      actions
    })
  })

  it('triggers the upload action', () => {
    const wrapper = shallowMount(FileUpload, { store, localVue })
    const input = wrapper.find('input')
    input.trigger('change')
    expect(actions.upload).toHaveBeenCalled()
  })
})
