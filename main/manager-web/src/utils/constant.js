const HAVE_NO_RESULT = '暂无'
export default {
    HAVE_NO_RESULT, // project_configuration_information
    PAGE: {
        LOGIN: '/login',
    },
    STORAGE_KEY: {
        TOKEN: 'TOKEN',
        PUBLIC_KEY: 'PUBLIC_KEY',
        USER_TYPE: 'USER_TYPE'
    },
    Lang: {
        'zh_cn': 'zh_cn', 'zh_tw': 'zh_tw', 'en': 'en'
    },
    FONT_SIZE: {
        'big': 'big',
        'normal': 'normal',
    }, // get_a_key_in_the_map
    get(map, key) {
        return map[key] || HAVE_NO_RESULT
    }
}
