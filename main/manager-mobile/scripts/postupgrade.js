// # implement `pnpm upgrade` will_be_upgraded_later `uniapp` related_dependencies
// # after_the_upgrade，a_lot_of_useless_dependencies_will_be_automatically_added，this_needs_to_be_deleted_to_reduce_the_size_of_the_dependent_package
// # just_execute_the_following_command

const { exec } = require('node:child_process')

// define_the_command_to_be_executed
const dependencies = [
  '@dcloudio/uni-app-harmony',
  // TODO: if_you_dont_need_a_small_program_for_a_certain_platform，please_delete_or_comment_out_manually
  '@dcloudio/uni-mp-alipay',
  '@dcloudio/uni-mp-baidu',
  '@dcloudio/uni-mp-jd',
  '@dcloudio/uni-mp-kuaishou',
  '@dcloudio/uni-mp-lark',
  '@dcloudio/uni-mp-qq',
  '@dcloudio/uni-mp-toutiao',
  '@dcloudio/uni-mp-xhs',
  '@dcloudio/uni-quickapp-webview',
  // i18n template needs to comment out the following
  'vue-i18n',
]

// use_exec_to_execute_commands
exec(`pnpm un ${dependencies.join(' ')}`, (error, stdout, stderr) => {
  if (error) {
    // if_there_is_an_error，print_error_message
    console.error(`execution_error: ${error}`)
    return
  }
  // print_normal_output
  console.log(`stdout: ${stdout}`)
  // if_there_is_an_error_output，also_print_it_out
  console.error(`stderr: ${stderr}`)
})
