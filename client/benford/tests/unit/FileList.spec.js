import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import FileList from '@/components/FileList.vue'

const localVue = createLocalVue()

localVue.use(Vuex)

describe('FileList.vue', () => {
  let store
  beforeEach(() => {
    store = new Vuex.Store({
      state: {
        files: {
          'census_2009b': {
            'delimiter': 'tab',
            'histogram': {}
          }
        }
      }
    })
  })

  it('renders a file list', () => {
    const wrapper = shallowMount(FileList, { store, localVue })
    expect(wrapper.text()).toContain('census_2009b')
  })
})
