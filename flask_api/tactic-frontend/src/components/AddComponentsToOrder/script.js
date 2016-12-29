import AddComponent from '../AddComponent/index.vue'

export default {
  name: 'AddComponentsToOrder',
  components: {
    'add-component': AddComponent
  },
  data () {
    return {
      number_of_components: null,
      number_of_components_options: this.get_component_count_options
    }
  }
}