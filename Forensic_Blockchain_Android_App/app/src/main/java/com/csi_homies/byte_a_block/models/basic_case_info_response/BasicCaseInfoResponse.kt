package com.csi_homies.byte_a_block.models.basic_case_info_response

import java.io.Serializable

data class BasicCaseInfoResponse(
    val cases: List<Case>
) : Serializable
