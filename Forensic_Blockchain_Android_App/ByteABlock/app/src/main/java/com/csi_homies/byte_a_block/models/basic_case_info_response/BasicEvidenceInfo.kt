package com.csi_homies.byte_a_block.models.basic_case_info_response

import java.io.Serializable

data class BasicEvidenceInfo(
    val evid_id: Int,
    val handler: String,
    val curr_status: String,
    val serial_no: String,
) : Serializable
