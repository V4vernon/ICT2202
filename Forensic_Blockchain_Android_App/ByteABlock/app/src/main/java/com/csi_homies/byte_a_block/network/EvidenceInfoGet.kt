package com.csi_homies.byte_a_block.network

import com.csi_homies.byte_a_block.models.evidence_info_response.EvidenceInfoResponse
import retrofit2.Call
import retrofit2.http.GET
import retrofit2.http.Headers
import retrofit2.http.Query

interface EvidenceInfoGet {
    @Headers("Connection:Close")
    @GET("api/view_evidence/")
    fun getEvidenceInfo(
        @Query("caseid") casid: String?,
        @Query("evidenceid") evidenceid:String?
    ): Call<EvidenceInfoResponse>
}