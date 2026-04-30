import axios from 'axios'

/**
 * Shared Axios instance for all API communications.
 * Configured with a base URL prefix to simplify relative endpoint calls.
 */
export const api = axios.create({
  baseURL: '/api'
})
