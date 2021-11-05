package com.csi_homies.byte_a_block.models.evidence_info_response

import java.io.Serializable

data class EvidenceInfoResponse(
    val case_id: Int,
    val curr_status: String,
    val evid_id: Int,
    val evid_type: String,
    val evidence_history: List<EvidenceHistory>,
    val handler: String,
    val image: String,
    val location: String,
    val notes: String,
    val serial_no: String
) : Serializable
