package com.csi_homies.byte_a_block.models.add_evidence_request

import java.io.Serializable

data class AddEvidencePostRequest(
    var case_id: Int,
    var handler: String,
    var draft_evid: List<DraftEvidenceInfo>,
) : Serializable
