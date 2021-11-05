package com.csi_homies.byte_a_block.models.evidence_info_response

import java.io.Serializable

data class EvidenceHistory(
    val handler: String,
    val purpose: String,
    val status: String,
    val date: Int
) : Serializable
