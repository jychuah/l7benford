import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import Histogram from '@/components/Histogram.vue'

const localVue = createLocalVue()

localVue.use(Vuex)

describe('Histogram.vue', () => {
  let store
  let actions
  beforeEach(() => {
    actions = {
      reparse: jest.fn(),
      selectField: jest.fn(),
    }
    store = new Vuex.Store({
      state: {
        selected: {
          filename: 'census_2009b',
          field: '7_2009',
          histogram: {},
          delimiter: 'tab'
        },
        files: {
          'census_2009b': {
            histogram: {
              '7_2009': {
                1: 0.3,
                2: 0.17,
                3: 0.12,
                4: 0.9,
                5: 0.8,
                6: 0.7,
                7: 0.6,
                8: 0.4,
                9: 0.3
              }
            }
          }
        }
      },
      actions
    })
  })

  it('renders the selected fields', () => {
    const wrapper = shallowMount(Histogram, { store, localVue })
    expect(wrapper.text()).toContain('census_2009b')
  })

  it('triggers the reparse action', () => {
    const wrapper = shallowMount(Histogram, { store, localVue })
    const input = wrapper.find('#delimiter-select')
    input.trigger('change')
    expect(actions.reparse).toHaveBeenCalled()
  })

  it('triggers the selectField action', () => {
    const wrapper = shallowMount(Histogram, { store, localVue })
    const input = wrapper.find('#field-select')
    input.trigger('change')
    expect(actions.selectField).toHaveBeenCalled()
  })
})
