// the_types_to_be_used_globally_are_placed_here

declare global {
  interface IResData<T> {
    code: number
    msg: string
    data: T
  }

  // uni.uploadFile file upload parameters
  interface IUniUploadFileOptions {
    file?: File
    files?: UniApp.UploadFileOptionFiles[]
    filePath?: string
    name?: string
    formData?: any
  }

  interface IUserInfo {
    nickname?: string
    avatar?: string
    /** wechat openid，nonwechat_does_not_have_this_field */
    openid?: string
    token?: string
  }
}

export {} // prevent_module_contamination
