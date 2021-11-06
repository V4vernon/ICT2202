package com.csi_homies.byte_a_block.models.add_evidence_request

import java.io.Serializable

data class DraftEvidenceInfo(
    var draft_evid_id: Int,
    var location: String,
    var evid_type: String,
    var serial_no: String,
    var image: String,
    var curr_status: String,
    var notes: String
) : Serializable
