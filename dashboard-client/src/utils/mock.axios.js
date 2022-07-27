/**
 * Axios Mocking instance
 */
 function AxiosMocking() {
    this.mockingEnabled = false
    this.mocks = []
}

/**
 * Add mock data
 * @param {Regex} urlPattern
 * @param {objecy} data
 */
AxiosMocking.prototype.addMock = function(urlPattern, data) {
    this.mocks.push({
        urlPattern: urlPattern,
        data: data
    })
}

/**
 * Get the mock data by the given URL.
 *
 * The system will loop through each registered URL pattern
 * to check if it matches to the given URL and return corresponding mock data.
 *
 * @param {string} url
 * @returns {object|null}
 */
AxiosMocking.prototype.getMockDataByUrl = function(url) {
    for (let i = 0; i < this.mocks.length; i++) {
        if (this.mocks[i].urlPattern.test(url)) {
            return this.mocks[i].data
        }
    }

    return null
}

/**
 * Set state of indicator mocking enabled
 * - Give `true` if you want to enable mocking
 * - Give `false` if you want to disable mocking
 *
 * @param {Boolean} state 
 */
AxiosMocking.prototype.enableMocking = function(state) {
    this.mockingEnabled = state;
}

/**
 * Check to see if this error is a mocked one
 *
 * @param {Error} error
 * @returns Boolean
 */
function isMockError(error) {
    return Boolean(error.mockData)
}

/**
 * Create new mock error
 *
 * @param {*} config The axios config
 * @param {*} mockData The mocked data
 * @returns Promise<T>
 */
const createMockError = function(config, mockData) {
    const mockError = new Error()
    mockError.mockData = mockData
    mockError.config = config
    return Promise.reject(mockError)
}

/**
 * Create new mock response from a mock error.
 * Mock data will be ingested from `mockError.mockData`
 *
 * @param {*} mockError Mock error
 * @returns Promise<T>
 */
const createMockResponse = function(mockError) {
    const { mockData, config } = mockError

    if (mockData.status && String(mockData.status)[0] !== '2') {
        // If there is mocked status and it is different from 2xx, then mock error response
        const err = new Error(mockData.message || 'mock error')
        err.code = mockData.status
        return Promise.reject(err)
    }

    // Handle mocked success
    return Promise.resolve(Object.assign({
        data: {},
        status: 200,
        statusText: 'OK',
        headers: {},
        config,
        isMock: true
    }, mockData))
}

/**
 * Intercept axios request and check to see if this request should be mocked or not.
 * If that, then throw a mock error. So that, we can mock response
 * via axios.interceptors.response
 *
 * @param {*} axios AxiosInstance
 * @param {*} mocking Mocking Instance - AxiosMocking
 */
function interceptRequest(axios, mocking) {
    axios.interceptors.request.use(config => {
        const mockData = mocking.getMockDataByUrl(config.url)
        if (mocking.mockingEnabled && !!mockData) {
            console.log('axios mocking ' + config.url)
            return createMockError(config, typeof mockData === "function" ? mockData(config) : mockData)
        }

        return config;
    }, error => Promise.reject(error))
}

/**
 * Intercept response to see if there is a mock error. If that, then we will mock response
 * and return to client
 *
 * @param {*} axios AxiosInstance
 */
function interceptResponse(axios) {
    axios.interceptors.response.use(response => response, error => {
        if (isMockError(error)) {
            return createMockResponse(error)
        }
        return Promise.reject(error)
    })
}

/**
 * Create and setup new axios mocking
 *
 * @param {*} axios AxiosInstance
 * @returns AxiosMocking
 */
export function createAxiosMocking(axios) {
    const mocking = new AxiosMocking()

    interceptRequest(axios, mocking)
    interceptResponse(axios)

    return mocking;
}