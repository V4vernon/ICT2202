package com.csi_homies.byte_a_block.utils

object Constants {
    // Pointing to the webserver
    const val BASE_URL: String = "http://167.71.205.211:5000/"
    const val SIGN_UP_URL: String = "${BASE_URL}register"

    const val CASE_INFO_ID: String = "case info"
    const val SELECTED_CASE_INFO_ID: String = "selected case info"
    const val SELECTED_CASE_NAME_ID: String = "selected case name"
    const val SELECTED_CASE_ID_ID: String = "selected case id"

    const val SELECTED_EVIDENCE_ID_ID: String = "selected evidence id"

    const val IMAGE_FILEPATH_ID: String = "image filepath"

    const val START_PHOTO_TAKING_ACTIVITY_ID: String = "take photo of evidence"
    const val ADD_NEW_EVIDENCE: Int = 50
    const val MODIFY_EVIDENCE_STATUS: Int = 60
}