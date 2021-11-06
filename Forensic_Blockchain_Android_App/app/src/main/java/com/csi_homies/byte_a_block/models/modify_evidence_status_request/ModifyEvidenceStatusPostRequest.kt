package com.csi_homies.byte_a_block.models.modify_evidence_status_request

import java.io.Serializable

data class ModifyEvidenceStatusPostRequest(
    var case_id: Int,
    var evid_id: Int,
    var handler: String,
    var new_status: String,
    var purpose: String,
    var image: String
) : Serializable
