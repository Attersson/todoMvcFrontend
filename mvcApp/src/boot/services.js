import Vue from 'vue'
import { restRequest } from './rest/request'

/**
 * Holds the references to each service.
 *
 */
const services = {
  testEnv: false,
  todos: {
    get (id) {
      return restRequest('https://cxtnfcdb07.execute-api.eu-central-1.amazonaws.com/default/GetTodo', 'POST', { id: id, a: null })
    },
    new () {
      return { completed: false }
    },
    list () {
      return restRequest('https://cxtnfcdb07.execute-api.eu-central-1.amazonaws.com/default/GetTodo', 'POST', { })
    },
    save (record) {
      return restRequest('https://974571mghl.execute-api.eu-central-1.amazonaws.com/default/TodoNew', 'POST', record)
    },
    update (id, record) {
      record.id = id
      return restRequest('https://wun7fqjene.execute-api.eu-central-1.amazonaws.com/default/EditTodo', 'PUT', record)
    },
    delete (id) {
      return restRequest('https://pm10holww4.execute-api.eu-central-1.amazonaws.com/default/DeleteTodo', 'DELETE', { id: id, a: null })
    }
  }
}

Vue.prototype.$services = services
