package com.csi_homies.byte_a_block.models.basic_case_info_response

import java.io.Serializable

data class Case(
    val case_name: String,
    val case_id: Int,
    val location: String,
    val date: Int,
    val case_status: String,
    val evidence: List<BasicEvidenceInfo>
) : Serializable